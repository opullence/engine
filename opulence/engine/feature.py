"""Example of a `feature` module in the package python_template.

This module contains two simple functions (`add` and `multiply`) operating on integers.
Each function is written using type hints: this means that we specify the type of each
variable within the function declaration. In this case, the inputs a and b are integers
and the output will be an integer.
"""


def add(a: int = 1, b: int = 2) -> int:
    """Example function that performs addition of two integers.

    Args:
        a (int): a first integer.
        b (int): a second integer.

    Returns:
        int: the addition of the two integers a and b.
    """
    return a + b


def multiply(a: int = 2, b: int = 2) -> int:
    """Example function that performs multiplication of two integers.

    Args:
        a (int): a first integer.
        b (int): a second integer.

    Returns:
        int: the multiplication of the two integers a and b.
    """
    return a * b
