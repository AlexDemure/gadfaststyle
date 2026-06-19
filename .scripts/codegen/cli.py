import ast

from common.collections import GENERATION_TITLES
from common.collections import OPERATION_TITLES
from common.collections import ROOT
from common.collections import TEMPLATES
from common.collections import GenerationType
from common.models import ModelInfo
from common.utils import attribute_value
from common.utils import pascal
from common.utils import run
from common.utils import snake


def model() -> None:
    import questionary

    model_value = questionary.text(
        "Введите название модели в PascalCase (например Account):",
    ).ask()
    if not model_value:
        return

    table = questionary.text(
        "Введите имя таблицы и файлов в snake_case (например account):",
        default=snake(model_value),
    ).ask()
    if not table:
        return

    collection = questionary.text(
        "Введите имя коллекции для HTTP-роутов в snake_case (например accounts):",
        default=f"{snake(table)}s",
    ).ask()
    if not collection:
        return

    run(
        path=TEMPLATES / "model",
        context={
            "model": pascal(model_value),
            "table": snake(table),
            "collection": snake(collection),
        },
        workdir=ROOT,
    )


def endpoint() -> None:
    import questionary

    folder = ROOT / "src/infrastructure/databases/postgres/tables"
    choices: list[ModelInfo] = []

    for path in sorted(folder.glob("*.py")):
        if path.name == "__init__.py":
            continue

        tree = ast.parse(path.read_text(encoding="utf-8"))

        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue

            if node.name == "Base":
                continue

            table = attribute_value(node, "__tablename__") or snake(node.name)
            collection = attribute_value(node, "__collection__") or f"{table}s"
            choices.append(
                ModelInfo(
                    model=node.name,
                    table=snake(table),
                    collection=snake(collection),
                ),
            )
            break

    choices.sort(key=lambda item: item.model)
    if not choices:
        print("ORM-модели не найдены. Сначала создайте модель.")
        return

    model_info = questionary.select(
        "Выберите модель, для которой нужно создать метод:",
        choices=[questionary.Choice(title=item.title, value=item) for item in choices],
    ).ask()
    operation = questionary.select(
        "Выберите, какой метод нужно создать:",
        choices=[questionary.Choice(title=title, value=value) for value, title in OPERATION_TITLES.items()],
    ).ask()
    if not model_info or not operation:
        return

    run(
        path=TEMPLATES / f"endpoint/{operation.value}",
        context={
            "model": model_info.model,
            "table": model_info.table,
            "collection": model_info.collection,
            "operation": operation.value,
        },
        workdir=ROOT,
    )


def main() -> None:
    import questionary

    action = questionary.select(
        "Что хотите создать?",
        choices=[questionary.Choice(title=title, value=value) for value, title in GENERATION_TITLES.items()],
    ).ask()
    if not action:
        return

    if action == GenerationType.MODEL:
        model()
        return

    endpoint()


if __name__ == "__main__":
    main()
