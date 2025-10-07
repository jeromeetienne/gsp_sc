from typing import Any

def fun()->Any:
    return 1

import typing
a = typing.cast(float, fun())

print(a)