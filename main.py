import importlib
import importlib.util
from os import system, name, walk
from time import sleep

print("Terminal for programs \n")


def generate_program_info():
    query = [
        ".git",
        ".idea",
        "__pycache__",
    ]

    _program_info = {}

    folder_names = next(walk('.'))[1]
    print(folder_names)

    for item in query:
        folder_names.remove(item)

    if folder_names:
        for folder in folder_names:
            for program in next(walk(f"./{folder}"))[2]:
                if 'main.py' in program:
                    _program_info[f"./{folder}/{program}"] = folder.replace('-', ' ').replace('_', ' ')

    print(_program_info)
    return _program_info


def generate_modules(_program_info):
    _modules = {}

    for item in _program_info:
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
                    except:
                        print("\nAn error occurred within the program")
                else:
                    unknown_counter += 1

            if _input_ == "ls":
                for program_string in program_strings:
                    print(program_strings[program_string])
                unknown_counter = 0

            if unknown_counter == len(command_info):
                print("\nUnknown command, please try again")
        except:
            print("\nQuitting...")
            break


program_info = generate_program_info()
modules = generate_modules(program_info)
terminal_params = generate_terminal_parameters(modules)


def main(_program_info):
    program_strings = {}

    if len(_program_info) > 0:
        for item in _program_info:
            item_info = _program_info[item]
            item_info = item_info.replace('_', ' ')
            program_strings[item] = f"""  Program Name: [{item}], 
    run command: [{item_info}]
"""

    print(f"""Current modules: {len(_program_info)}

Programs:""")
    if program_strings == {}:
        print('None')
    else:
        for program_string in program_strings:
            print(program_strings[program_string])
        print("Activating Terminal\n")
        terminal("quit()", terminal_params, program_strings)


if __name__ == '__main__':
    main(program_info)
