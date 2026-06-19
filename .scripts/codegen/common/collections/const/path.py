import pathlib


CURRENT = pathlib.Path(__file__).resolve().parents[3]
ROOT = CURRENT.parents[1]
TEMPLATES = CURRENT / "templates"
