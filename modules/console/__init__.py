import datetime
from modules.console.formats import TEXT_FORMATS

def clear():
    print("\033[H\033[J")

def log(message):
    time = datetime.datetime.now().strftime("%Y %m %d | %H:%M:%S")

    print(f'<{TEXT_FORMATS.UNDERLINE}{time}{TEXT_FORMATS.ENDC}> [   LOG   ] {message}{TEXT_FORMATS.ENDC}.')

def success(message):
    time = datetime.datetime.now().strftime("%Y %m %d | %H:%M:%S")

    print(f'<{TEXT_FORMATS.UNDERLINE}{time}{TEXT_FORMATS.ENDC}> [ {TEXT_FORMATS.OKGREEN}SUCCESS{TEXT_FORMATS.ENDC} ] {message}{TEXT_FORMATS.ENDC}.')

def warn(message):
    time = datetime.datetime.now().strftime("%Y %m %d | %H:%M:%S")

    print(f'<{TEXT_FORMATS.UNDERLINE}{time}{TEXT_FORMATS.ENDC}> [ {TEXT_FORMATS.WARNING}  WARN {TEXT_FORMATS.ENDC} ] {message}{TEXT_FORMATS.ENDC}.')

def error(message):
    time = datetime.datetime.now().strftime("%Y %m %d | %H:%M:%S")

    print(f'<{TEXT_FORMATS.UNDERLINE}{time}{TEXT_FORMATS.ENDC}> [ {TEXT_FORMATS.FAIL} ERROR {TEXT_FORMATS.ENDC} ] {message}{TEXT_FORMATS.ENDC}.')