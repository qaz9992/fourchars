from typing import Any, Final
from sys import argv
from typing_extensions import Annotated
from lists import *

Usage: Final[str] = "Usage: python . [file(.fc)] (-h/--help)\n-h/--help: Show this message and exit"

ERROR: Final[int] = 1
EXIT: Final[int] = 0
CODE_EXIT: Final[int] = 0

memory: List3D = List3D(100, 0)
pointer: Pos = Pos(0, 0, 0)
ive: bool = True
ae: bool = True

class ExitError(Exception): ...
def inpvalueerror(de: bool) -> None:
    global ive
    if de:
        ive = True
    else:
        ive = False
    return
def auto_exit(de: bool) -> None:
    global ae
    if de:
        ae = True
    else:
        ae = False
    return


todo = {
    "input:ValueError:disable:": lambda: inpvalueerror(False),
    "input:ValueError:enable:": lambda: inpvalueerror(True),
    "auto:exit:enable:": lambda: auto_exit(True),
    "auto:exit:disable:": lambda: auto_exit(False)
}

def four_char_a_group(code: str) -> list[str]:
    return [code[i:i+4] for i in range(0, len(code), 4)]

def main(argv: list, argc: int) -> Any:
    if (argc < 2) or ('--help' in argv) or ('-h' in argv):
        print(Usage)
        return ERROR
    
    file_path = argv[1]

    try:
        with open(file_path, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return ERROR
    
    code = code.replace('\n', '')
    for i in todo.keys():
        if i in code:
            todo[i]()
            code = code.replace(i, '')
    
    code = four_char_a_group(code)

    if code[-1].__len__() < 4:
        print("Error: The last group of characters is less than 4 characters long.")
        return ERROR
    if code[0] != "main":
        print("Error: The first group of characters must be 'main'.")
        return ERROR
    
    for command in code[1:]:
        if command == "exit":
            return CODE_EXIT
        if command[0] == 'm':
            _value = int(command[2:], 16)
            if command[1] == 'u':
                pointer.add_to_y(_value)
            elif command[1] == 'd':
                pointer.add_to_y(-_value)
            elif command[1] == 'l':
                pointer.add_to_x(-_value)
            elif command[1] == 'r':
                pointer.add_to_x(_value)
        elif command[0] == 'l':
            _value = int(command[2:], 16)
            if command[1] == 'u':
                pointer.add_to_z(_value)
            elif command[1] == 'd':
                pointer.add_to_z(-_value)
        elif command[0] == '=':
            if command[1] == 'n':
                memory.set(pointer.x, pointer.y, pointer.z, int(command[2:], 16))
            elif command[1] == 'a':
                memory.set(pointer.x, pointer.y, pointer.z, ord(command[2]))
        elif command[0] == 'p':
            if command[1] == 'n':
                print(memory.get(pointer.x, pointer.y, pointer.z), end='')
            elif command[1] == 'a':
                if command[2] != ' ':
                    for i in range(int(command[2:], 16)):
                        print(chr(memory.get(pointer.x, pointer.y, pointer.z)), end='')
                else:
                    print(chr(memory.get(pointer.x, pointer.y, pointer.z)), end='')

            elif command[1] == 'l':
                print()
        elif command[0] == '+':
            if command[1] == 'n':
                memory.set(pointer.x, pointer.y, pointer.z, memory.get(pointer.x, pointer.y, pointer.z) + int(command[2:], 16))
            elif command[1] == 'm':
                if command[2] == 'l':
                    memory.set(pointer.x, pointer.y, pointer.z, memory.get(pointer.x, pointer.y, pointer.z) + memory.get(pointer.x - 1, pointer.y, pointer.z))
                elif command[2] == 'r':
                    memory.set(pointer.x, pointer.y, pointer.z, memory.get(pointer.x, pointer.y, pointer.z) + memory.get(pointer.x + 1, pointer.y, pointer.z))
                elif command[2] == 'u':
                    memory.set(pointer.x, pointer.y, pointer.z, memory.get(pointer.x, pointer.y, pointer.z) + memory.get(pointer.x, pointer.y - 1, pointer.z))
                elif command[2] == 'd':
                    memory.set(pointer.x, pointer.y, pointer.z, memory.get(pointer.x, pointer.y, pointer.z) + memory.get(pointer.x, pointer.y + 1, pointer.z))
        elif command[0] == '#':
            continue
        elif command[0] == 'i':
            if command[1] == 'a':
                user_input = input()
                memory.set(pointer.x, pointer.y, pointer.z, ord(user_input[0]) if user_input else 0)
            elif command[1] == 'n':
                try:
                    user_input = int(input())
                except ValueError:
                    if ive:
                        print("Error: Invalid input. Expected an integer.")
                        return ERROR
                    else:
                        user_input = -1
                memory.set(pointer.x, pointer.y, pointer.z, user_input)
    if ae:
        return EXIT
    else:
        raise ExitError("Program did not exit properly.")

if __name__ == '__main__':
    main(argv, len(argv))