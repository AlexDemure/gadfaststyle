import re


REGEXP_NON_ALPHANUMERIC = re.compile(r"[^0-9A-Za-z]+")
REGEXP_PASCAL_WORDS = re.compile(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+")
