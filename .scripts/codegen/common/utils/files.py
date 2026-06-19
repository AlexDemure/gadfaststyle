import pathlib


def write(path: pathlib.Path, content: str, mode: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if mode == "w" and path.exists():
        return

    if mode == "a":
        prefix = "\n" if path.exists() and path.read_text(encoding="utf-8").strip() else ""
        with path.open("a", encoding="utf-8") as file:
            file.write(f"{prefix}{content}")
        return

    if mode == "p":
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            return

        current = path.read_text(encoding="utf-8")
        suffix = "\n" if current.strip() else ""
        path.write_text(f"{content}{suffix}{current}", encoding="utf-8")
        return

    if mode in {"w", "ow"}:
        path.write_text(content, encoding="utf-8")
        return

    raise ValueError(f"Unsupported mode: {mode}")
