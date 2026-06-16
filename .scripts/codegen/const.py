import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
TESTS = ROOT / "tests"
TEMPLATES = pathlib.Path(__file__).resolve().parent / "templates"
LINT = ROOT / ".scripts/lints/configs"

OPERATIONS = [
    "one",
    "list",
    "paginated",
    "create",
    "update",
    "delete",
    "exists",
]

MODEL_FILES = {
    "src/infrastructure/databases/postgres/tables/{singular}.py": "model/src/infrastructure/databases/postgres/tables/table.tmpl",
    "src/infrastructure/databases/postgres/crud/{singular}.py": "model/src/infrastructure/databases/postgres/crud/crud.tmpl",
    "src/domain/models/{singular}.py": "model/src/domain/models/model.tmpl",
    "src/domain/collections/exceptions/{singular}.py": "model/src/domain/collections/exceptions/error.tmpl",
    "src/infrastructure/databases/postgres/adapters/repositories/{singular}.py": "model/src/infrastructure/databases/postgres/adapters/repositories/repository.tmpl",
    "src/application/utils/{singular}.py": "model/src/application/utils/utils.tmpl",
    "src/entrypoints/http/public/routers/{collection}/registry.py": "model/src/entrypoints/http/public/routers/registry.tmpl",
    "src/entrypoints/http/public/schemas/{singular}.py": "model/src/entrypoints/http/public/schemas/header.tmpl",
    "tests/factories/infrastructure/databases/postgres/tables/{singular}.py": "model/tests/factories/infrastructure/databases/postgres/tables/table_factory.tmpl",
    "tests/factories/domain/models/{singular}.py": "model/tests/factories/domain/models/model_factory.tmpl",
}

MODEL_EXPORTS = [
    ("src/infrastructure/databases/postgres/tables/__init__.py", "from .{singular} import {entity}"),
    ("src/infrastructure/databases/postgres/crud/__init__.py", "from .{singular} import {entity}"),
    ("src/domain/models/__init__.py", "from .{singular} import {entity}"),
    ("src/domain/collections/exceptions/__init__.py", "from .{singular} import {entity}NotFound"),
    ("src/domain/collections/__init__.py", "from .exceptions import {entity}NotFound"),
    ("src/infrastructure/databases/postgres/adapters/repositories/__init__.py", "from .{singular} import {entity}"),
    (
        "tests/factories/infrastructure/databases/postgres/tables/__init__.py",
        "from .{singular} import {entity}",
    ),
    ("tests/factories/domain/models/__init__.py", "from .{singular} import {entity}"),
]

ENDPOINT_FILES = {
    "src/application/usecases/{collection}/{op}.py": "endpoint/{op}/src/application/usecases/{op}.tmpl",
    "src/entrypoints/http/public/deps/{collection}/{op}.py": "endpoint/{op}/src/entrypoints/http/public/deps/{op}.tmpl",
    "src/entrypoints/http/public/routers/{collection}/{op}.py": "endpoint/{op}/src/entrypoints/http/public/routers/{op}.tmpl",
    "tests/test_integrations/test_entrypoints/test_http/test_public/test_{collection}/test_{op}.py": "endpoint/{op}/tests/test_integrations/test_entrypoints/test_http/test_public/{op}.tmpl",
}

SCHEMA_BLOCKS = {
    "one": {
        "classes": ["{entity}"],
        "templates": ["endpoint/one/src/entrypoints/http/public/schemas/entity.tmpl"],
    },
    "list": {
        "classes": ["{entity}", "Search{entity}"],
        "templates": [
            "endpoint/list/src/entrypoints/http/public/schemas/entity.tmpl",
            "endpoint/list/src/entrypoints/http/public/schemas/search.tmpl",
        ],
    },
    "paginated": {
        "classes": ["{entity}", "Search{entity}", "{plural}"],
        "templates": [
            "endpoint/paginated/src/entrypoints/http/public/schemas/entity.tmpl",
            "endpoint/paginated/src/entrypoints/http/public/schemas/search.tmpl",
            "endpoint/paginated/src/entrypoints/http/public/schemas/plural.tmpl",
        ],
    },
    "create": {
        "classes": ["{entity}", "Create{entity}"],
        "templates": [
            "endpoint/create/src/entrypoints/http/public/schemas/entity.tmpl",
            "endpoint/create/src/entrypoints/http/public/schemas/create.tmpl",
        ],
    },
    "update": {
        "classes": ["Update{entity}"],
        "templates": ["endpoint/update/src/entrypoints/http/public/schemas/update.tmpl"],
    },
    "delete": {
        "classes": ["Delete{entity}"],
        "templates": ["endpoint/delete/src/entrypoints/http/public/schemas/delete.tmpl"],
    },
    "exists": {
        "classes": ["Exists{entity}"],
        "templates": ["endpoint/exists/src/entrypoints/http/public/schemas/exists.tmpl"],
    },
}
