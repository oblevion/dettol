class Trace:
    def __init__(self):
        self.steps = []
        self.verification = None

    def add_step(self, subproblem, tool, answer, reasoning):
        self.steps.append({
            'subproblem': subproblem,
            'tool': tool,
            'answer': answer,
            'reasoning': reasoning
        })

    def add_verification(self, is_valid):
        self.verification = is_valid

    def generate_report(self):
        report = ""
        for i, step in enumerate(self.steps):
            report += f"Step {i+1}: {step['subproblem']} [Tool: {step['tool']}] >> {step['answer']}\n  Reasoning: {step['reasoning']}\n"
        report += f"Verification: {self.verification}\n"
        return report
