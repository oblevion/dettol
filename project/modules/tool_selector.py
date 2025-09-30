def select_tool(subproblem):
    # Simple keyword-based selection
    if any(keyword in subproblem.lower() for keyword in ["all", "none", "if", "then", "implies"]):
        return "symbolic"
    else:
        return "llm"
