# how to beautify that? 
import sys, os
sys.path.insert(0, '../')

from parse import pid, period, docile, naughty, verbose
from config import path_to_storage
from colored_text import colored

def count_cpu_usage(pid):

    clock_tick = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

    with open(f"/proc/{pid}/stat", "r") as f:
        stat = f.readline().strip('\n').split(" ")
    
    with open("/proc/uptime", "r") as f:
        system_uptime_sec = int(float(f.readline().strip('\n').split(" ")[0]))
    
    process_utime_sec = int(stat[13]) / clock_tick
    process_stime_sec = int(stat[14]) / clock_tick
    process_starttime_sec = int(stat[21]) / clock_tick

    process_elapsed_sec = system_uptime_sec - process_starttime_sec
    process_usage_sec = process_utime_sec + process_stime_sec
    proess_usage = process_usage_sec * 100 / process_elapsed_sec

    return (process_usage_sec, proess_usage)


# colored.print_cyan(path_to_storage)
with open(f"/proc/{pid}/status") as f:
    process_name = f.readline().strip('\n').split(":\t")[1]

# total = 16294880 

if verbose:
    colored.print_cyan(f"{pid} {process_name}")
    colored.print_cyan(f"Conduct survey {docile} + {naughty} times each {period} seconds")
    res = count_cpu_usage(pid)
    colored.print_cyan(f"{res[0]} {res[1]}")