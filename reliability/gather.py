from dataclasses import dataclass
import pandas as pd
from metrics.cpu import momentary_cpu_usage
from metrics.children import number_of_children
from metrics.memory import mem_top
from time import sleep

@dataclass
class Metric:
    cpu_usage: float
    memory_usage: float
    number_of_children: int
    process_class: int # 0 - docile, 1 - naughty


def metrics_generator(pid, period, number, process_class):
    for _ in range(number):
        sleep(period)
        yield Metric(momentary_cpu_usage(pid), mem_top(pid)*100, number_of_children(pid), process_class)


def df_generator(pid, period, number, process_class):
    df = pd.DataFrame(metrics_generator(pid, number, period, process_class))
    return df