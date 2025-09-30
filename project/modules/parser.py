def decompose_problem(question):
    # Rule-based decomposition example
    if "if" in question and "," in question:
        clauses = question.split(",")
        return [clause.strip() for clause in clauses]
    else:
        return [question]
