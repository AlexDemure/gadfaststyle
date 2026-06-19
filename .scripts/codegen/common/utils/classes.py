import ast


def attribute_value(node: ast.ClassDef, key: str) -> str | None:
    for statement in node.body:
        if not isinstance(statement, ast.Assign):
            continue

        for target in statement.targets:
            if not isinstance(target, ast.Name) or target.id != key:
                continue

            if isinstance(statement.value, ast.Constant) and isinstance(statement.value.value, str):
                return statement.value.value

    return None
