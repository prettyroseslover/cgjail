import os

clock_tick = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

pid = 2983

with open(f"/proc/{pid}/stat", "r") as f:
	stat = f.readline().strip('\n').split(" ")

process_utime = int(stat[13])
process_stime = int(stat[14])
process_starttime = int(stat[21])

# print(f"{process_utime} {type(process_utime)}")
# print(f"{process_starttime} {type(process_starttime)}")

with open("/proc/uptime", "r") as f:
	system_uptime_sec = int(float(f.readline().strip('\n').split(" ")[0]))

process_utime_sec = process_utime / clock_tick
process_stime_sec = process_stime / clock_tick
process_starttime_sec = process_starttime / clock_tick

process_elapsed_sec = system_uptime_sec - process_starttime_sec
process_usage_sec = process_utime_sec + process_stime_sec
proess_usage = process_usage_sec * 100 / process_elapsed_sec



print(f"The PID {pid} has spent {process_utime_sec} s in user mode\n{process_stime_sec} s in kernel mode.\nTotal CPU usage is {process_usage_sec} s.\nProcess has used {proess_usage}% of CPU")
