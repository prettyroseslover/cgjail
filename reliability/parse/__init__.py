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
        raise argparse.ArgumentTypeError(f'No such PID as {pid}')
    return pid


def positive_int(x):
    n = int(x)
    if n <= 0:
        raise argparse.ArgumentTypeError('Negative values are not allowed')
    return n


def is_csv(x):
    import csv
    try:
        with open(x) as file:
            csv.reader(file)
            return True
    except csv.Error:
        return False


def csv_file(x):
    from os.path import exists
    if not exists(x):
        raise argparse.ArgumentTypeError(f'File {x} does not exist')
    if not is_csv(x):
        raise argparse.ArgumentTypeError('Specified file is not a valid CSV file')
    return x


parser = CustomArgumentParser(description='Script to prepare data and train kNN-model for a given piece of software')

parser.add_argument('-v', '--verbosity', action = "store_true")

subparsers = parser.add_subparsers(dest='step', required=True)

docile_parser = subparsers.add_parser('docile')
naughty_parser = subparsers.add_parser('naughty')
train_parser = subparsers.add_parser('train')

docile_parser.add_argument('-p', '--pid', required=True, type=pid, help='PID of a docile process')
docile_parser.add_argument('-T', '--period', default=0, type=positive_int, help='Survey period in seconds')
docile_parser.add_argument('-n', '--number', default=50, type=positive_int, help='Number of data point to gather per docile process')

naughty_parser.add_argument('-p', '--pid', required=True, type=pid, help='PID of a naughty process')
naughty_parser.add_argument('-T', '--period', default=0, type=positive_int, help='Survey period in seconds')
naughty_parser.add_argument('-n', '--number', default=50, type=positive_int, help='Number of data point to gather per naughty process')
naughty_parser.add_argument('-o', '--output', required=True, type=csv_file, help='CSV file to append naughty data to')

train_parser.add_argument('-i', '--input', required=True, type=csv_file, help='CSV file to train a model')

args = parser.parse_args()

verbose = args.verbosity


