import re


REGEXP_NON_ALPHANUMERIC = re.compile(r"[^a-zA-Z0-9]")
REGEXP_PASCAL_WORDS = re.compile(r"[A-Z]{2,}(?=[A-Z][a-z]|[0-9]|$)|[A-Z]?[a-z0-9]+|[A-Z]+|[0-9]+")
