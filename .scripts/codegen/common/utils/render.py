import pathlib
import shlex
import shutil
import subprocess
import typing

from .files import write
from .jinja import render
from .yaml import load


def resolve_context(
    current: dict[str, typing.Any],
    extra: dict[str, typing.Any],
) -> dict[str, typing.Any]:
    resolved = dict(current)

    for key, value in extra.items():
        if isinstance(value, str):
            resolved[key] = render(value, resolved)
            continue

        resolved[key] = value

    return resolved


def apply(path: pathlib.Path, context: dict[str, typing.Any], workdir: pathlib.Path) -> None:
    config = load(path)
    local_context = resolve_context(context, config.get("context", {}))

    for folder in config.get("folders", []):
        target = workdir / render(folder, local_context)
        target.mkdir(parents=True, exist_ok=True)

    for item in config.get("files", []):
        target = workdir / render(item["path"], local_context)
        content = render(item["content"], local_context)
        mode = item.get("mode", "w")
        write(target, content, mode)

    for script in config.get("scripts", []):
        command = render(script["command"], local_context)
        args = shlex.split(command)
        if not args:
            continue

        if shutil.which(args[0]) is None:
            continue

        subprocess.run(
            args,
            cwd=workdir,
            check=script.get("check", False),
        )


def run(path: pathlib.Path, context: dict[str, typing.Any], workdir: pathlib.Path) -> None:
    if path.is_dir():
        for item in sorted(path.rglob("*.yaml")):
            apply(path=item, context=context, workdir=workdir)
        return

    apply(path=path, context=context, workdir=workdir)
