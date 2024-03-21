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

def positive_int(x):
    n = int(x)
    if n <= 0:
        raise ValueError('Negative values are not allowed')
    return n

parser = CustomArgumentParser(description='Script to prepare data and train kNN-model for a given process')
parser.add_argument('-p', '--pid', required=True, type=pid, help='PID of a process')
parser.add_argument('-T', '--period', default=0, type=positive_int, help='Survey period in seconds')
parser.add_argument('-d', '--docile', default=50, type=positive_int, help='Number of data point to gather per docile process')
parser.add_argument('-n', '--naughty', default=50, type=positive_int, help='Number of data point to gather per naughty process')
parser.add_argument('-v', '--verbosity', action = "store_true")

args = parser.parse_args()

pid = args.pid
period = args.period
docile = args.docile
naughty = args.naughty
verbose = args.verbosity
