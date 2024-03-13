# how to beautify that? 
import sys
sys.path.insert(0, '../')

from parse import pid
from config import path_to_storage
from colored_text import colored

# colored.print_cyan(path_to_storage)
with open(f"/proc/{pid}/status") as f:
    process_name = f.readline().strip('\n').split(":\t")[1]

colored.print_cyan(f"{pid} {process_name}")

total = 16294880 