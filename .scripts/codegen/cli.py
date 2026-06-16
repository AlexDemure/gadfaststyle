import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import typing

import jinja2
import questionary


CURRENT = pathlib.Path(__file__).resolve().parent

if str(CURRENT) not in sys.path:
    sys.path.insert(0, str(CURRENT))

if str(CURRENT.parents[1]) not in sys.path:
    sys.path.insert(0, str(CURRENT.parents[1]))

import const

from utils import pascal
from utils import snake


ENVIRONMENT = jinja2.Environment(autoescape=False, keep_trailing_newline=True)


def render(template: str, context: dict[str, typing.Any]) -> str:
    source = (const.TEMPLATES / template).read_text(encoding="utf-8")
    return ENVIRONMENT.from_string(source).render(context)


def write(target: pathlib.Path, content: str, append: bool = False) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)

    if not append and target.exists():
        return

    mode = "a" if append else "w"
    prefix = "\n" if append and target.exists() and target.read_text(encoding="utf-8").strip() else ""

    with target.open(mode=mode, encoding="utf-8") as file:
        file.write(f"{prefix}{content}")


def prepend(target: pathlib.Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    current = target.read_text(encoding="utf-8") if target.exists() else ""
    prefix = "\n\n" if current.strip() else ""
    target.write_text(f"{content}{prefix}{current}", encoding="utf-8")


def ensure_package(folder: pathlib.Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    init = folder / "__init__.py"

    if init.exists():
        return

    if "test_" in folder.name:
        init.write_text("__all__: list[str] = []\n", encoding="utf-8")
        return

    init.touch()


def export(path: pathlib.Path, line: str) -> None:
    write(path, f"{line}\n", append=True)


def has_class(path: pathlib.Path, name: str) -> bool:
    if not path.exists():
        return False

    pattern = rf"^class {re.escape(name)}\b"
    return bool(re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE))


def format_code() -> None:
    commands: list[str] = []

    if shutil.which("isort"):
        commands.append(f"isort .scripts/codegen src tests --settings-path {const.LINT}")

    if shutil.which("ruff"):
        commands.extend(
            [
                f"ruff check --fix .scripts/codegen src tests --no-cache --config {const.LINT / 'ruff.toml'}",
                f"ruff format .scripts/codegen src tests --no-cache --config {const.LINT / 'ruff.toml'}",
            ]
        )

    for command in commands:
        subprocess.run(shlex.split(command), cwd=const.ROOT, check=False)


def models() -> list[str]:
    from src.infrastructure.databases.orm.sqlalchemy.tables import Base
    from src.infrastructure.databases.postgres import tables

    found: list[str] = []

    for name in dir(tables):
        candidate = getattr(tables, name)
        if isinstance(candidate, type) and issubclass(candidate, Base) and candidate is not Base:
            found.append(name)

    return sorted(set(found))


def build_context(entity: str, singular: str, collection: str, op: str) -> dict[str, str]:
    return {
        "collection": collection,
        "entity": entity,
        "op": op,
        "plural": pascal(collection),
        "singular": singular,
    }


def template_path(template: str, context: dict[str, str]) -> str:
    return template.format(**context)


def ensure_schema(context: dict[str, str]) -> pathlib.Path:
    schema = const.SRC / f"entrypoints/http/public/schemas/{context['singular']}.py"
    imports = render(f"endpoint/{context['op']}/src/entrypoints/http/public/schemas/imports.tmpl", context)

    if not schema.exists():
        write(schema, "")
        return schema

    prepend(schema, imports)

    return schema


def export_schemas(context: dict[str, str], classes: list[str]) -> None:
    registry = const.SRC / "entrypoints/http/public/schemas/__init__.py"

    for schema_class in classes:
        export(registry, f"from .{context['singular']} import {schema_class}")


def update_router_registry(collection: str, op: str, entity: str) -> None:
    folder = const.SRC / f"entrypoints/http/public/routers/{collection}"
    ensure_package(folder)

    registry = folder / "registry.py"

    if not registry.exists():
        write(
            registry,
            "from src.framework.routing import APIRouter\n\n\nrouter = APIRouter()\n",
        )
        write(folder / "__init__.py", 'from .registry import router\n\n\n__all__ = [\n    "router",\n]\n')

    export(registry, f"from . import {op}")
    export(registry, f"router.include_router({op}.router)")

    public = const.SRC / "entrypoints/http/public/routers/registry.py"
    export(public, f"from . import {collection}")
    export(public, f'router.include_router({collection}.router, tags=["{entity}"])')


def ensure_http_entrypoints(context: dict[str, str]) -> None:
    ensure_package(const.SRC / f"application/usecases/{context['collection']}")
    ensure_package(const.SRC / f"entrypoints/http/public/deps/{context['collection']}")

    for target, template in const.MODEL_FILES.items():
        if not target.startswith("src/entrypoints/http/public/"):
            continue

        path = const.ROOT / target.format(**context)
        if path.exists():
            continue

        if "schemas/" in target:
            write(path, "")
            continue

        write(path, render(template_path(template, context), context))

    folder = const.SRC / f"entrypoints/http/public/routers/{context['collection']}"
    init = folder / "__init__.py"

    if not init.exists():
        write(init, 'from .registry import router\n\n\n__all__ = [\n    "router",\n]\n')

    public = const.SRC / "entrypoints/http/public/routers/registry.py"
    export(public, f"from . import {context['collection']}")
    export(public, f'router.include_router({context["collection"]}.router, tags=["{context["entity"]}"])')


def generate_model(singular: str, entity: str) -> None:
    context = build_context(entity=entity, singular=singular, collection=f"{singular}s", op="model")

    ensure_http_entrypoints(context)

    for target, template in const.MODEL_FILES.items():
        if target.startswith("src/entrypoints/http/public/"):
            continue

        write(const.ROOT / target.format(**context), render(template_path(template, context), context))

    for target, line in const.MODEL_EXPORTS:
        export(const.ROOT / target, line.format(entity=entity, singular=singular))

    format_code()
    print(f"model {entity} generated")


def generate_endpoint(entity: str, singular: str, collection: str, op: str) -> None:
    context = build_context(entity=entity, singular=singular, collection=collection, op=op)

    ensure_http_entrypoints(context)

    ensure_package(const.SRC / f"entrypoints/http/public/deps/{collection}")
    ensure_package(const.SRC / f"entrypoints/http/public/routers/{collection}")
    ensure_package(const.TESTS / f"test_integrations/test_entrypoints/test_http/test_public/test_{collection}")

    for target, template in const.ENDPOINT_FILES.items():
        write(const.ROOT / target.format(**context), render(template_path(template, context), context))

    schema = ensure_schema(context)
    block = const.SCHEMA_BLOCKS[op]

    for schema_class, template in zip(block["classes"], block["templates"], strict=True):
        rendered_class = schema_class.format(**context)
        if has_class(schema, rendered_class):
            continue

        write(schema, render(template_path(template, context), context), append=True)

    export_schemas(context, [schema_class.format(**context) for schema_class in block["classes"]])
    update_router_registry(collection=collection, op=op, entity=entity)

    format_code()
    print(f"endpoint {collection}:{op} generated")


def model() -> None:
    singular = questionary.text("snake_case (files/table):").ask()
    if not singular:
        return

    entity = questionary.text("PascalCase (class):", default=pascal(singular)).ask()
    if not entity:
        return

    generate_model(snake(singular), entity)


def endpoint() -> None:
    choices = models()
    if not choices:
        print("No models found. Generate a model first.")
        return

    entity = questionary.select("Model:", choices=choices).ask()
    operation = questionary.select("Endpoint:", choices=const.OPERATIONS).ask()

    if not entity or not operation:
        return

    singular = questionary.text("snake_case (files):", default=snake(entity)).ask()
    collection = questionary.text("collection (snake_case):", default=f"{snake(entity)}s").ask()

    if not singular or not collection:
        return

    generate_endpoint(entity=entity, singular=snake(singular), collection=snake(collection), op=operation)


def main() -> None:
    if questionary.select("Generate:", choices=["model", "endpoint"]).ask() == "model":
        model()
        return

    endpoint()


if __name__ == "__main__":
    main()
