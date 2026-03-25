from typing import Any, Final
from sys import argv as arg

ERROR: Final[int] = 1

def main(argv: list, argc: int) -> Any:
    try:
        with open(argv[1], 'r') as f:
            code = f.read()
    except IndexError:
        print("Usage: python main.py <filename>")
        return ERROR

if __name__ == '__main__':
    main(arg, len(arg))