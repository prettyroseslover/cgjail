import sys
sys.path.insert(0, '../') # how to beautify that? 
from parse import verbose, args
from config import path_to_storage
from colored_text import colored

if verbose:
    colored.print_cyan(f"==ON THE {args.step.upper()} STEP==")

if args.step == 'train':
    from train import Model
    input = args.input
    K = args.k_neighbour
    kNN = Model(input, path_to_storage, K)
    kNN.train_and_save()
    if verbose:
        colored.print_cyan(kNN.quality())
    exit()

process_class = int(args.step != 'docile')
pid = args.pid
period = args.period
number = args.number

with open(f"/proc/{pid}/status") as f:
    process_name = f.readline().strip('\n').split(":\t")[1]

if verbose:
    colored.print_cyan("You've chosen process:")
    colored.print_cyan(f"{pid} {process_name}")

from gather import df_generator
df = df_generator(pid, number, period, process_class)

if verbose:
    print(df.head())

if args.step == 'naughty':
    output = args.output
    df.to_csv(output, mode='a', index=False, header=False)
    colored.print_green(f"Results are appended to {output}")
    exit()

csv_file = f"{path_to_storage}/{process_name}.csv"
df.to_csv(csv_file, index=False)
colored.print_green(f"Results are written to {csv_file}")