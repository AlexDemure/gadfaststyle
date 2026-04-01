import typing

from jinja2 import Template


def generate(file: str, context: dict[str, typing.Any]) -> str:
    with open(file) as _file:
        template = Template(_file.read())
    return template.render(context)
