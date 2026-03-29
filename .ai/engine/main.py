from __future__ import annotations

from pathlib import Path
import sys


def _bootstrap() -> None:
    engine_root = Path(__file__).resolve().parent
    src_dir = engine_root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


def main() -> int:
    _bootstrap()
    from cli.main import main as cli_main

    return cli_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
