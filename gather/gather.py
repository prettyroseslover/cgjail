# how to beautify that? 
import sys
sys.path.insert(0, '../')

from parse import pid, period, docile, naughty, verbose
from metrics.cpu import momentary_cpu_usage
from metrics.children import children
from metrics.memory import pss_bytes, rss_bytes, memtotal_bytes, mem_top
from config import path_to_storage
from colored_text import colored


with open(f"/proc/{pid}/status") as f:
    process_name = f.readline().strip('\n').split(":\t")[1]


if verbose:
    #colored.print_cyan(f"{pid} {process_name}")
    # colored.print_cyan(f"Conduct survey {docile} + {naughty} times each {period} seconds")

    #colored.print_cyan(pss_bytes(pid))
    #colored.print_cyan(rss_bytes(pid))
    #colored.print_cyan(memtotal_bytes())

    #print(mem_top(pid) * 100)

    '''
    for i in range(10):
        colored.print_cyan(f"{momentary_cpu_usage(pid)}")
    '''
     
    
    colored.print_cyan(children(pid))


