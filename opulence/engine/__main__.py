import argparse
import sys

from opulence.engine.feature import add, multiply


def get_argument_parser() -> argparse.ArgumentParser:
    """Create the cmdline argument parser"""

    parser = argparse.ArgumentParser()
    parser.add_argument("a", help="A first integer", type=int)
    parser.add_argument("b", help="A second integer", type=int)

    return parser


def main():
    args = get_argument_parser().parse_args()

    print("a + b = {}".format(add(args.a, args.b)))
    print("a * b = {}".format(multiply(args.a, args.b)))


if __name__ == "__main__":
    sys.exit(main())
