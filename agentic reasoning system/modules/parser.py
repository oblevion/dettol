def decompose_problem(question):
    if "if" in question and "," in question:
        clauses = question.split(",")
        return [clause.strip() for clause in clauses]
    elif "and" in question and "," not in question:
        return [clause.strip() for clause in question.split("and")]
    else:
        return [question]
