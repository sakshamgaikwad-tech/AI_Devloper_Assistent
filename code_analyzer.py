import ast

def analyze_python_code(code: str):
    result = {
        "lines": len(code.split("\n")),
        "functions": [],
        "classes": []
    }

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                result["functions"].append(node.name)

            if isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)

    except Exception:
        result["error"] = "Could not analyze code"

    return result