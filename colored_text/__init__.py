class colored:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def print_red(text):
        print(f"{colored.RED}{text}{colored.ENDC}")

    def print_yellow(text):
        print(f"{colored.YELLOW}{text}{colored.ENDC}")

    def print_green(text):
        print(f"{colored.GREEN}{text}{colored.ENDC}")

    def print_blue(text):
        print(f"{colored.BLUE}{text}{colored.ENDC}")

    def print_cyan(text):
        print(f"{colored.CYAN}{text}{colored.ENDC}")