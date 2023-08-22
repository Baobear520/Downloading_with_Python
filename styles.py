from colored import Fore, Back, Style

def color_info_message(message):
    print(f'{Fore.black}{Back.yellow}{message}{Style.reset}')

def color_error_message(message):
    print(f'{Fore.black}{Back.red}{message}{Style.reset}')