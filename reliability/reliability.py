import sys
sys.path.insert(0, '../') # how to beautify that? 
from parse import verbose, args
from config import path_to_storage
from colored_text import colored
from gather import df_generator

#import pandas as pd

if args.step == 'train':
    csv_file = args.input
    print(f"TRAIN: {csv_file}")
    exit()

process_class = int(args.step != 'docile')
pid = args.pid
period = args.period
number = args.number

with open(f"/proc/{pid}/status") as f:
    process_name = f.readline().strip('\n').split(":\t")[1]

if verbose:
    colored.print_cyan(f"==ON THE {args.step} STEP==")
    colored.print_cyan("You've chosen process:")
    colored.print_cyan(f"{pid} {process_name}")


csv_file = f"{path_to_storage}/{process_name}.csv"
df = df_generator(pid, number, period, process_class)

if verbose:
    print(df.head())


df.to_csv(csv_file, index=False)
colored.print_green(f"Results are written to {csv_file}")