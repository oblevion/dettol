def select_tool(subproblem):
    keywords = ["all", "none", "if", "then", "implies", "cannot", "never", "always"]
    if any(k in subproblem.lower() for k in keywords):
        return "symbolic"
    return "llm"
