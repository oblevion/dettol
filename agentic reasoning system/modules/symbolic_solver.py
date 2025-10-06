def solve_symbolically(subproblem):
    neg_keywords = ["not", "never", "cannot", "impossible", "no"]
    all_keywords = ["all", "every", "always", "each"]
    some_keywords = ["some", "may", "might", "possible"]

    sub_lower = subproblem.lower()
    if any(k in sub_lower for k in neg_keywords):
        answer = 5  # Negative answer choice (customize per dataset)
    elif any(k in sub_lower for k in all_keywords):
        answer = 1  # Affirmative choice
    elif any(k in sub_lower for k in some_keywords):
        answer = 2  # Intermediate choice
    else:
        answer = 1  # Default fallback
    reasoning = f"Symbolic heuristic for '{subproblem}': answer {answer}"
    return answer, reasoning
