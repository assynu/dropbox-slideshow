import datetime

class TextFormats:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Clear():
    print("\033[H\033[J")

def log_message(message_type, message, color):
    time = datetime.datetime.now().strftime("%Y %m %d | %H:%M:%S")
    print(f'<{TextFormats.UNDERLINE}{time}{TextFormats.ENDC}> [ {color}{message_type}{TextFormats.ENDC} ] {message}{TextFormats.ENDC}.')

def Log(message):
    log_message("LOG", message, TextFormats.OKBLUE)

def Success(message):
    log_message("SUCCESS", message, TextFormats.OKGREEN)

def Warn(message):
    log_message("WARN", message, TextFormats.WARNING)

def Error(message):
    log_message("ERROR", message, TextFormats.FAIL)