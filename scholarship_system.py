"""Student Scholarship Eligibility Screener.

This module evaluates scholarship applicants based on academic GPA,
extracurricular credits, and family income against defined threshold cutoffs.
"""

import ast
import json
import operator
from typing import Any, Dict, List, Optional

results: Dict[str, Dict[str, Any]] = {}
MERIT_FORMULA = "gpa * 10 + credits * 2"
INCOME_LIMIT = 800000
CUTOFF = 85

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval_node(node: ast.AST, variables: Dict[str, float]) -> float:
    """Recursively evaluates an AST arithmetic node with strict safety checks."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id in variables:
            return float(variables[node.id])
        raise ValueError(f"Undefined variable in formula: {node.id}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            left = _safe_eval_node(node.left, variables)
            right = _safe_eval_node(node.right, variables)
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            operand = _safe_eval_node(node.operand, variables)
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    raise ValueError(f"Unsupported syntax expression: {type(node).__name__}")


def calculate_merit_score(gpa: float, credits: float) -> float:
    """Calculates applicant merit score securely without arbitrary code execution."""
    variables = {"gpa": float(gpa), "credits": float(credits)}
    try:
        parsed_ast = ast.parse(MERIT_FORMULA, mode="eval")
        return round(_safe_eval_node(parsed_ast.body, variables), 2)
    except (SyntaxError, ValueError, KeyError):
        return round(float(gpa) * 10.0 + float(credits) * 2.0, 2)


def evaluate_applicant(
    student_id: str,
    test_scores: Dict[str, Any],
    logs: Optional[List[str]] = None,
) -> bool:
    """Evaluates applicant eligibility based on merit score and income limit."""
    if logs is None:
        logs = []

    gpa = float(test_scores.get("gpa", 0.0))
    credits = float(test_scores.get("credits", 0))
    income = float(test_scores.get("income", 0))

    score = calculate_merit_score(gpa, credits)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    results[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula: str) -> None:
    """Updates the merit evaluation formula string safely."""
    global MERIT_FORMULA  # pylint: disable=global-statement
    test_ast = ast.parse(new_formula, mode="eval")
    _safe_eval_node(test_ast.body, {"gpa": 8.0, "credits": 2.0})
    MERIT_FORMULA = new_formula


def persist_results(file: str = "scholarships.json") -> None:
    """Serializes evaluation results to a JSON file using a context manager."""
    with open(file, "w", encoding="utf-8") as file_handle:
        json.dump(results, file_handle, indent=2)


def load_results(file: str = "scholarships.json") -> None:
    """Loads evaluation results from a JSON file safely."""
    global results  # pylint: disable=global-statement
    try:
        with open(file, "r", encoding="utf-8") as file_handle:
            results = json.load(file_handle)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass


def print_shortlist() -> None:
    """Displays all applicants shortlisted for scholarships."""
    print("Shortlisted applicants:")
    for student_id, details in results.items():
        if details.get("eligible"):
            print(f"  {student_id} score = {details.get(score)}")


printShortlist = print_shortlist


def main() -> None:
    """Main execution entry point."""
    evaluate_applicant("U001", {"gpa": 9.1, "credits": 4, "income": 450000})
    evaluate_applicant("U002", {"gpa": 7.2, "credits": 1, "income": 300000})
    evaluate_applicant("U003", {"gpa": 12.5, "credits": -3, "income": -1})
    evaluate_applicant("U004", {"gpa": 6.5})

    try:
        formula = input("Merit formula (Enter to keep default): ").strip()
        if formula:
            change_formula(formula)
    except (EOFError, KeyboardInterrupt, ValueError):
        pass

    evaluate_applicant("U005", {"gpa": 8.4, "credits": 3, "income": 600000})
    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
