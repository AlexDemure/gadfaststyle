from fastapi import Header


def dependency(language: str = Header(default="en", alias="accept-language")) -> str:
    return language
