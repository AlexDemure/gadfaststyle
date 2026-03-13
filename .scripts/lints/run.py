import ast
import os
import pathlib
import subprocess

import typer


app = typer.Typer()


def getmodules(file: pathlib.Path) -> list[str]:
    with file.open("r", encoding="utf-8") as _file:
        tree = ast.parse(_file.read(), filename=str(file))

    modules = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            for name in node.names:
                if not name.name.startswith("_"):
                    modules.append(name.asname or name.name)

    return sorted(set(modules))


def addimports(file: pathlib.Path, modules: list[str]) -> None:
    with file.open("r", encoding="utf-8") as _file:
        lines = _file.readlines()

    imports = []
    skip = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("__all__"):
            skip = True
            continue
        if skip:
            # Пропускаем до конца списка
            if "]" in stripped:
                skip = False
            continue
        imports.append(line)

    # Добавим новый __all__ в конец
    imports.append("__all__ = [\n")
    for name in sorted(modules):
        imports.append(f'    "{name}",\n')
    imports.append("]\n")

    with file.open("w", encoding="utf-8") as _file:
        _file.writelines(imports)


def fiximports(directory: pathlib.Path) -> None:
    for dirpath, dirnames, filenames in os.walk(directory):
        dirnames[:] = [dirname for dirname in dirnames if dirname not in {".venv", ".volumes"}]
        for filename in filenames:
            if filename == "__init__.py":
                modules = getmodules(pathlib.Path(dirpath) / filename)
                if modules:
                    addimports(pathlib.Path(dirpath) / filename, modules)


@app.command()
def lint(path: pathlib.Path | None = typer.Option(None)) -> None:
    if not path:
        path = pathlib.Path.cwd()

    config = pathlib.Path(__file__).parent / "configs"

    fiximports(path)

    commands = [
        ["isort", str(path), "--settings-path", str(config)],
        ["ruff", "check", "--fix", str(path), "--no-cache", "--config", str(config / "ruff.toml")],
        ["ruff", "format", str(path), "--no-cache", "--config", str(config / "ruff.toml")],
        ["mypy", str(path), "--config-file", str(config / "setup.cfg")],
    ]

    for command in commands:
        subprocess.run(command, check=False)


if __name__ == "__main__":
    app()
