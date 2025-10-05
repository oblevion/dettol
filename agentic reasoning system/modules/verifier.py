def verify_solution(subproblems, answers):
    # Basic check: ensure no contradictory answers in negated clauses
    for sub, ans in zip(subproblems, answers):
        if "not" in sub.lower() and ans == 1:
            return False
    return all(a is not None for a in answers)
