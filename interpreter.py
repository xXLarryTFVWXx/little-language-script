from re import A
import os, sys, random
from opcodes import *

# custom language interpreter defined in custom scripting language.txt
# examples in example.txt
# list of valid extensions in extensions.txt

# verifies extension and grabs which mode to use.
def verify_extension(filename)-> tuple[int, str]:
    extension_location = filename.find(".lls") or filename.find(".lsb")
    if extension_location == -1:
        return -5, "Invalid Extension"
    mode_start = filename.find(".", extension_location-3, extension_location)
    if mode_start == -1:
        return -5, "Invalid Extension"
    mode = int(filename[mode_start+1:extension_location])
    return mode, ("bytes" if filename[-1] == "b" else "text")

    
# interactive interpreter
def interpret() -> int:
    while True:
        in_line = input(f"lls:{os.getcwd()}> ").split()
        # stitch strings back together
        in_string = False
        string : str = ""
        if len(in_line) == 0:
            continue
        completed_line: list[str|bool|int] = []
        for index, word in enumerate(in_line):
            string = word if not in_string else string + word
            in_string = (word.startswith('"') and not in_string)
            if word.endswith('"') and in_string:
                string += word
                in_string = False
            completed_line.append(string)
        match completed_line:
            case ("!exit",):
                return -1
            case ("!exit", code):
                return_code: int = int(code)
                return return_code or -1
            case _:
                print("Invalid command.")
        print(completed_line)

EXIT_CODES = {
    -5: "Invalid Extension",
    -4: "Implicit Exit without Code: Invalid Instruction",
    -3: "Implicit Exit without Code: Error Undefined",
    -2: "Invalid Exit Code",
    -1: "Explicit Exit without Code",
    0: "Implicit Exit without Code: No Errors"
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arguments = sys.argv[1:]
        for argument in arguments:
            if argument == "-h" or argument == "--help":
                print("Help: This script interprets the lls file given as an argument. If no argument is given, it will open up the interpreter. It will only run if the file has a .lls extension.")
                sys.exit(0)
            else:
                bit_width, mode = verify_extension(argument)
                if mode.lower() == "bytes":
                    with open(argument, "rb") as file:
                        data = file.read()
                if mode.lower() == "text":
                    with open(argument, "r") as file:
                        data = file.read()
    else:
        exit_code: int = interpret()
        print(EXIT_CODES.get(exit_code, "Invalid Exit Code"))
        sys.exit(exit_code)