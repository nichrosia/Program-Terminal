print("Terminal for programs \n")

import importlib
from os import system, name, listdir
from time import sleep


def generate_program_info():
    query = [
        "main.py",
    ]

    program_info = {}

    filenames = listdir()

    for item in query:
        filenames.remove(item)

    if filenames != []:
        for program in filenames:
            program_info[program] = f"{program.replace('.py', '')}"

    return program_info


def generate_terminal_parameters(program_info, modules):
    terminal_params = {}
    for command in modules:
        terminal_params[command] = modules[command].main
    return terminal_params


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


def terminal(breaksignal, command_info):
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
        _input_ = input("\nProgram Command: ")

        if _input_ == breaksignal:
            break  # breaks loop

        unknown_counter = 0
        for command in command_info:
            program = command_info[command]
            if _input_ == command:
              try:
                program()
              except:
                print("\nAn error occured within the program")
            else:
                unknown_counter += 1

        if unknown_counter == len(command_info):
            print("\nUnknown command, please try again")
      except:
        print("\nQuitting...")
        break


def generate_modules(program_info):
    modules = {}
    for item in program_info:
        modules[item.replace(".py",
                             '').replace('_', ' ')] = importlib.import_module(
                                 item.replace(".py", ""), f".{item}")
    return modules


program_info = generate_program_info()
modules = generate_modules(program_info)
terminal_params = generate_terminal_parameters(program_info, modules)

# ending code

# events = pygame.event.get()
# for event in events:
# if event.type == pygame.KEYDOWN:
# if event.key == pygame.K_LCTRL and pygame.K_l or event.key == pygame.K_RCTRL and pygame.K_l:
# clear()


def main(program_info):
    program_strings = {}

    if len(program_info) > 0:
        for item in program_info:
            item_info = program_info[item]
            item_info = item_info.replace('_', ' ')
            program_strings[
                item] = f"  Program Name: [{item}], \n  run command: [{item_info}]\n"

    print(f"Current modules: {len(program_info)}\n\nPrograms:")
    for program_string in program_strings:
        print(program_strings[program_string])
    print("Activating Terminal\n")
    terminal("quit()", terminal_params)

    # terminal("quit()", modules)


if __name__ == '__main__':
    main(program_info)
