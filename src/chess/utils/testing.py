"""Util to test inputs from generate scripts."""

import typing


def test_input(
    generation: typing.Callable,
    occurences: int = 20,
    in_between_character: str = "",
):
    """Prints in console *occurences* number of *generation* generated str.

    Args:
        generation (typing.Callable): Function used to generate str. (can be
            lambda)
        occurences (int, optional): Number of inputs in console. Defaults to
            20.
        in_between_character (str, optional): Character between inputs.
            (can be \\n). Defaults to "".
    """
    for i in range(occurences):
        print(f"{in_between_character}{generation()}")
