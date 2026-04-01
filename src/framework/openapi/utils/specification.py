import typing

from src.framework.openapi.collections import SPECIFICATION_COMPONENTS_SCHEMAS_REF_KEY
from src.framework.openapi.collections import SPECIFICATION_COMPONENTS_SCHEMAS_REF_PATH
from src.framework.openapi.collections import SPECIFICATION_PATHS_RESPONSES_CONTENT
from src.framework.openapi.collections import SPECIFICATION_PATHS_RESPONSES_CONTENT_APPLICATION_JSON
from src.framework.openapi.collections import SPECIFICATION_PATHS_RESPONSES_CONTENT_APPLICATION_JSON_EXAMPLE


def findrefs(openapi: dict[str, typing.Any] | list[dict[str, typing.Any]], find: str, replace: str) -> None:
    if isinstance(openapi, dict):
        for key, value in openapi.items():
            if (
                key == SPECIFICATION_COMPONENTS_SCHEMAS_REF_KEY
                and value == f"{SPECIFICATION_COMPONENTS_SCHEMAS_REF_PATH}{find}"
            ):
                openapi[key] = f"{SPECIFICATION_COMPONENTS_SCHEMAS_REF_PATH}{replace}"
            else:
                findrefs(value, find, replace)
    elif isinstance(openapi, list):
        for item in openapi:
            findrefs(item, find, replace)


def errors(*args: typing.Any) -> dict[int | str, dict[str, typing.Any]]:
    _responses, _grouped = {}, {}

    for error in [arg() for arg in args]:
        if error.code not in _grouped:
            _grouped[error.code] = []
        _grouped[error.code].append(error.http)

    for code, examples in _grouped.items():
        _responses[code] = {
            SPECIFICATION_PATHS_RESPONSES_CONTENT: {
                SPECIFICATION_PATHS_RESPONSES_CONTENT_APPLICATION_JSON: {
                    SPECIFICATION_PATHS_RESPONSES_CONTENT_APPLICATION_JSON_EXAMPLE: examples
                    if len(examples) > 1
                    else examples[0]
                }
            }
        }

    return _responses
