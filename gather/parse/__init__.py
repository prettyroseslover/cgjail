import argparse, psutil
from colored_text import colored

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        colored.print_red(f"Error: {message}")
        self.print_usage()
        exit()

def pid(x):
    pid = int(x)
    if not psutil.pid_exists(pid):
        raise ValueError('No such PID')
    return pid

parser = CustomArgumentParser(description='Script to prepare data and train kNN-model for a given process')
parser.add_argument('-p', '--pid', required=True, type=pid, help='PID of a process')

args = parser.parse_args()