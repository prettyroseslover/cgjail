import os
from time import sleep

def primitive_cpu_usage(pid):

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


def momentary_cpu_usage(pid): 

    clock_tick = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

    with open(f"/proc/{pid}/stat", "r") as f:
        stat = f.readline().strip('\n').split(" ")

    with open("/proc/uptime", "r") as f:
        system_uptime_sec_1 = int(float(f.readline().strip('\n').split(" ")[0]))

    process_utime_sec_1 = int(stat[13]) / clock_tick
    process_stime_sec_1 = int(stat[14]) / clock_tick
    process_starttime_sec_1 = int(stat[21]) / clock_tick
    process_usage_sec_1 = process_utime_sec_1 + process_stime_sec_1
    process_elapsed_sec_1 = system_uptime_sec_1 - process_starttime_sec_1

    sleep(2)

    with open(f"/proc/{pid}/stat", "r") as f:
        stat = f.readline().strip('\n').split(" ")

    with open("/proc/uptime", "r") as f:
        system_uptime_sec_2 = int(float(f.readline().strip('\n').split(" ")[0]))

    process_utime_sec_2 = int(stat[13]) / clock_tick
    process_stime_sec_2 = int(stat[14]) / clock_tick
    process_starttime_sec_2 = int(stat[21]) / clock_tick
    process_usage_sec_2 = process_utime_sec_2 + process_stime_sec_2
    process_elapsed_sec_2 = system_uptime_sec_2 - process_starttime_sec_2
    
    return (process_usage_sec_2 - process_usage_sec_1) * 100 / (process_elapsed_sec_2 - process_elapsed_sec_1)