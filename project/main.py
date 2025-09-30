from modules.parser import decompose_problem
from modules.tool_selector import select_tool
from modules.symbolic_solver import solve_symbolically
from modules.base_llm_interface import solve_with_llm
from modules.verifier import verify_solution
from modules.trace_generator import Trace

def agentic_reasoning_system(question):
    # Step 1: Decompose problem
    subproblems = decompose_problem(question)

    trace = Trace()
    answers = []

    for sub in subproblems:
        # Step 2: Select tool per subproblem
        tool = select_tool(sub)

        # Step 3: Execute subproblem with chosen tool
        if tool == "symbolic":
            answer, reasoning = solve_symbolically(sub)
        elif tool == "llm":
            answer, reasoning = solve_with_llm(sub)
        else:
            answer, reasoning = "Not implemented", ""

        trace.add_step(sub, tool, answer, reasoning)
        answers.append(answer)

    # Step 4: Verification
    is_valid = verify_solution(subproblems, answers)
    trace.add_verification(is_valid)

    # Step 5: Human-readable trace output
    return trace.generate_report(), answers, is_valid
