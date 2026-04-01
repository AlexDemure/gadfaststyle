import sys
import typing


def name(stream: typing.TextIO) -> str:
    if stream is sys.stdout:
        return "stdout"
    elif stream is sys.stderr:
        return "stderr"
    else:
        raise NotImplementedError
