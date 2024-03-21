import re, os

def regex(line):
    if re.search('^Pss:', line):
        number = line.strip('\n').split(" ")[-2]
        return int(number)

def pss_bytes(pid):

    with open(f"/proc/{pid}/smaps", "r") as f:
        pss = sum(list(filter(None, map(regex, f))))
    
    return pss * 1024


def rss_bytes(pid):
    page_size = os.sysconf(os.sysconf_names['SC_PAGESIZE'])
   
    with open(f"/proc/{pid}/statm", "r") as f:
        rss_pages = int(f.readline().strip('\n').split(" ")[1])
    
    rss_bytes = page_size * rss_pages

    return rss_bytes


def memtotal_bytes():

    with open(f"/proc/meminfo") as f:
        memtotal = int(f.readline().strip('\n').split(" ")[-2])
    
    return memtotal * 1024


def mem_top(pid):
    return rss_bytes(pid)/memtotal_bytes()