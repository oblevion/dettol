
# Agentic Reasoning System for Logic QA

A modular, explainable system for multi-step logic question answering. It decomposes problems into subproblems, selects a solver per subproblem (symbolic rules or LLM stub), records reasoning traces, verifies consistency, and predicts a final answer using a hybrid of training-pattern overrides and confidence-weighted aggregation. Predictions and traces are written to `output.csv`.

## Features

- Problem decomposition into subproblems (`parser.py`).
- Heuristic tool selection between symbolic solver and LLM stub (`tool_selector.py`).
- Symbolic solver tuned for negation, universals, and possibility cues (`symbolic_solver.py`).
- Confidence-weighted aggregation of subanswers and training-pattern override (`main.py`).
- Trace logging of each step and verification (`trace_generator.py`, `verifier.py`).
- Robust CSV loader tolerant to delimiter/format inconsistencies (`main.py`).
- Output CSV columns: `topic`, `problem_statement`, `solution`, `correct option`.

## Repository Structure

```
.
├── main.py
├── requirements.txt
├──configs
    └── system_config.yaml
├── README.md
├── modules/
│   ├── parser.py
│   ├── tool_selector.py
│   ├── symbolic_solver.py
│   ├── base_llm_interface.py
│   ├── verifier.py
│   └── trace_generator.py
├── datasets/
│   ├── train.csv
│   └── test.csv
└── output.csv
```

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Data Format

CSV columns expected:
- `problemstatement`
- `topic`
- `answeroption1`, `answeroption2`, ...
- `correctoptionnumber` (required in train.csv, optional in test.csv)

## How It Works

1. Load datasets with robust parsing (CSV/TSV fallback) in `main.py`.
2. Build a pattern-to-answer map from `train.csv` using the first five words of `problemstatement` as key phrases.
3. For each problem:
   - Decompose into subproblems (`parser.py`).
   - Select tool per subproblem (`tool_selector.py`).
   - Solve subproblems with rules in `symbolic_solver.py` and a stub for LLM in `base_llm_interface.py`.
   - Record each step (tool, answer, reasoning) to a trace (`trace_generator.py`).
   - Run basic verification (`verifier.py`).
4. Prediction: pattern override if key phrase known, else weighted aggregation by confidence.
5. Save results to `output.csv` and print training accuracy if applicable.

## Usage

```bash
python main.py
```

Results and traces written to `output.csv`.

## Output Example

| topic      | problem_statement                                                  | solution                                                            | correct option |
|------------|--------------------------------------------------------------------|---------------------------------------------------------------------|---------------|
| Quantifiers| If all mammals breathe air, and whales are mammals, do whales ... | Predicted option: 1 | Trace: Step 1: ... | Verification: True             | 1             |

## Customization

- Tune keywords and mapping in `modules/symbolic_solver.py`.
- Extend/modify tool selection logic in `modules/tool_selector.py`.
- Improve confidence functions and pattern mapping in `main.py`.


## Acknowledgments

Expert systems, multi-step reasoning, and modular agentic frameworks.
