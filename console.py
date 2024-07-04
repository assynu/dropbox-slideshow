import datetime

class TextFormats:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    warnING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def send_message(message_type, message, color):
    time = datetime.datetime.now().strftime("%Y %m %d | %H:%M:%S")
    print(f'<{TextFormats.UNDERLINE}{time}{TextFormats.ENDC}> [ {color}{message_type}{TextFormats.ENDC} ] {message}{TextFormats.ENDC}.')

def clear():
    print("\033[H\033[J")

def log(message):
    send_message("Log", message, TextFormats.OKBLUE)

def success(message):
    send_message("Success", message, TextFormats.OKGREEN)

def warn(message):
    send_message("Warn", message, TextFormats.warnING)

def error(message):
    send_message("Error", message, TextFormats.FAIL)