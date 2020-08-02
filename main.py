import importlib
import importlib.util
from os import system, name, walk
from time import sleep

print("Terminal for programs \n")


def generateprogram_info():
    exclude_list = [
        ".git",
        ".idea",
        "__pycache__",
    ]

    program_info = {}

    folder_names = next(walk('.'))[1]
    print(folder_names)

    folder_names = [folder_name for folder_name in folder_names if folder_name not in exclude_list]

    if folder_names:
        for folder in folder_names:
            for program in next(walk(f"./{folder}"))[2]:
                if 'main.py' in program:
                    program_info[f"./{folder}/{program}"] = folder.replace('-', ' ').replace('_', ' ')

    print(program_info)
    return program_info


def generate_modules(program_info):
    _modules = {}

    for item in program_info:
        name = program_info[item]

        spec = importlib.util.spec_from_file_location("module.name", item)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        _modules[name] = mod
    return _modules


def generate_terminal_parameters(_modules):
    terminal_parameters = {}
    for command in _modules:
        terminal_parameters[command] = _modules[command].main
    return terminal_parameters


def clear():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def reset():
    clear()
    for i in range(3):
        sleep(0.15)
        clear()
        print(f"\nFatal Exception.\n\nResetting{'.' * (i + 1)}")
    sleep(0.15)
    clear()


def terminal(breaksignal, command_info, program_strings):
    """ breaksignal is a string which ends the terminal
    command info is a dictionary containing commands and the program it runs
    terminal example:
      {
        command: program name
        'fraction to decimal': main
      }
    both parameters are required

    programs that are detected must have a main function to work, otherwise it will cause an error
    """
    while True:
        try:
            _input_ = input("\n$ ")

            if _input_ == breaksignal:
                break  # breaks loop

            unknown_counter = 0
            for command in command_info:
                program = command_info[command]
                if _input_ == command:
                    try:
                        program()
                    except Exception:
                        print("\nAn error occurred within the program")
                else:
                    unknown_counter += 1

            if _input_ == "ls":
                for program_string in program_strings:
                    print(program_strings[program_string])
                unknown_counter = 0

            if unknown_counter == len(command_info):
                print("\nUnknown command, please try again")
        except Exception:
            print("\nQuitting...")
            break


def main():
    program_info = generateprogram_info()
    print(program_info)
    modules = generate_modules(program_info)
    terminal_params = generate_terminal_parameters(modules)

    program_strings = {}

    if len(program_info) > 0:
        for item in program_info:
            item_info = program_info[item]
            item_info = item_info.replace('_', ' ')
            program_strings[item] = (
                f"  Program Name: [{item}], \n"
                f"    run command: [{item_info}]\n"
            )

    print(
        f"Current modules: {len(program_info)}\n\n"
        "Programs:\n"
    )
    if len(program_strings) == 0:
        print('None')
    else:
        for program_string in program_strings:
            print(program_strings[program_string])
        print("Activating Terminal\n")
        terminal("quit()", terminal_params, program_strings)


if __name__ == '__main__':
    main()
