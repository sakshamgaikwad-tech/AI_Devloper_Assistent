import ast

def detect_bugs(code: str):
    issues = []

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            # detect empty functions
            if isinstance(node, ast.FunctionDef):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    issues.append(f"Function '{node.name}' is empty")

            # detect too many arguments
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 5:
                    issues.append(
                        f"Function '{node.name}' has too many parameters"
                    )

            # detect print debugging
            if isinstance(node, ast.Call):
                if getattr(node.func, "id", None) == "print":
                    issues.append("Possible debug print statement found")

    except Exception as e:
        issues.append(f"Code parsing error: {str(e)}")

    return issues