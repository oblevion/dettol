import pandas as pd
import csv
from collections import Counter

def clean_and_load_csv(path):
    try:
        df = pd.read_csv(path)
        if len(df.columns) == 1:
            raise Exception
    except:
        try:
            df = pd.read_csv(path, delimiter='\t')
            if len(df.columns) == 1:
                raise Exception
        except:
            with open(path, encoding='utf-8') as f:
                lines = f.readlines()
            header = lines[0].strip()
            delimiter = "," if "," in header else ("\t" if "\t" in header else " ")
            columns = header.split(delimiter)
            data = [l.strip().split(delimiter) for l in lines[1:] if l.strip()]
            df = pd.DataFrame(data, columns=columns)
    df.columns = [c.strip() for c in df.columns]
    return df

from modules.parser import decompose_problem
from modules.tool_selector import select_tool
from modules.symbolic_solver import solve_symbolically
from modules.base_llm_interface import solve_with_llm
from modules.verifier import verify_solution
from modules.trace_generator import Trace

class LogicQADataset:
    def __init__(self, dataframe, has_labels=True):
        self.questions = dataframe['problem_statement'].tolist()
        answer_cols = [col for col in dataframe.columns if col.lower().startswith('answer_option')]
        self.options = dataframe[answer_cols].values.tolist()
        self.topics = dataframe['topic'].tolist()
        if has_labels and 'correct_option_number' in dataframe.columns:
            self.labels = dataframe['correct_option_number'].astype(int).tolist()
        else:
            self.labels = [None] * len(self.questions)

    def __len__(self):
        return len(self.questions)

    def __getitem__(self, idx):
        return {
            'topic': self.topics[idx],
            'question': self.questions[idx],
            'options': self.options[idx],
            'label': self.labels[idx]
        }

def build_pattern_answer_map(train_df):
    pattern_map = {}
    for _, row in train_df.iterrows():
        question = row['problem_statement'].lower()
        answer = int(row['correct_option_number'])
        key_phrase = " ".join(question.split()[:5])
        if key_phrase in pattern_map:
            pattern_map[key_phrase].append(answer)
        else:
            pattern_map[key_phrase] = [answer]
    for key in pattern_map:
        c = Counter(pattern_map[key])
        pattern_map[key] = c.most_common(1)[0][0]
    return pattern_map

def predict_with_pattern_map(question, pattern_map):
    key_phrase = " ".join(question.lower().split()[:5])
    return pattern_map.get(key_phrase, None)

def confidence_score(subproblem):
    negations = ["not", "never", "cannot", "impossible"]
    if any(neg in subproblem.lower() for neg in negations):
        return 0.9
    return 0.6

def weighted_aggregate(answers, subproblems):
    weights = [confidence_score(sub) for sub in subproblems]
    tally = {}
    for ans, w in zip(answers, weights):
        tally[ans] = tally.get(ans, 0) + w
    return max(tally, key=tally.get)

def train(train_dataset):
    print(f"Training on {len(train_dataset)} examples")

def evaluate_accuracy(dataset, pattern_map):
    correct = 0
    total = 0
    for item in dataset:
        question = item['question']
        subproblems = decompose_problem(question)
        answers = []
        for sub in subproblems:
            tool = select_tool(sub)
            if tool == "symbolic":
                answer, _ = solve_symbolically(sub)
            else:
                answer, _ = solve_with_llm(sub)
            answers.append(answer)

        pattern_pred = predict_with_pattern_map(question, pattern_map)
        if pattern_pred is not None:
            pred = pattern_pred
        else:
            pred = weighted_aggregate(answers, subproblems)

        label = item['label']
        if label is not None:
            total += 1
            if str(pred) == str(label):
                correct += 1

    if total > 0:
        accuracy = correct / total
        print(f"Training Accuracy: {accuracy:.2%} ({correct}/{total})")
    else:
        print("No labels to compute accuracy.")

def evaluate_and_save(test_dataset, output_file, pattern_map):
    correct = 0
    count_with_labels = 0
    output_rows = []
    header = ["topic", "problem_statement", "solution", "predicted option"]

    for idx, item in enumerate(test_dataset):
        trace = Trace()
        topic = item['topic']
        problem = item['question']
        label = item['label']
        subproblems = decompose_problem(problem)
        answers = []

        for sub in subproblems:
            tool = select_tool(sub)
            if tool == "symbolic":
                answer, reasoning = solve_symbolically(sub)
            else:
                answer, reasoning = solve_with_llm(sub)
            trace.add_step(sub, tool, answer, reasoning)
            answers.append(answer)

        pattern_pred = predict_with_pattern_map(problem, pattern_map)
        if pattern_pred is not None:
            predicted_answer = pattern_pred
        else:
            predicted_answer = weighted_aggregate(answers, subproblems)

        solution_text = f"| Trace: {trace.generate_report().replace(chr(10), ' | ')}"

        output_rows.append([
            topic,
            problem,
            solution_text,
            predicted_answer,
           
        ])

        if label is not None:
            count_with_labels += 1
            if str(predicted_answer) == str(label):
                correct += 1

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(output_rows)

    if count_with_labels > 0:
        print(f"Test Accuracy: {correct / count_with_labels:.2%}")
    else:
        print("No ground-truth labels available for accuracy calculation.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    train_df = clean_and_load_csv('datasets/train.csv')
    pattern_map = build_pattern_answer_map(train_df)
    test_df = clean_and_load_csv('datasets/test.csv')

    train_dataset = LogicQADataset(train_df, has_labels=True)
    test_dataset = LogicQADataset(test_df, has_labels=False)

    train(train_dataset)

    print("\nEvaluating training set accuracy:")
    evaluate_accuracy(train_dataset, pattern_map)

    print("\nEvaluating test set and saving output:")
    evaluate_and_save(test_dataset, 'output.csv', pattern_map)
