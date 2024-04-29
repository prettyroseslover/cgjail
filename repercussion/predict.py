from dataclasses import dataclass
import pandas as pd
from metrics.cpu import momentary_cpu_usage
from metrics.children import number_of_children
from metrics.memory import mem_top

@dataclass
class Metric:
    cpu_usage: float
    memory_usage: float
    number_of_children: int

def current_metrics(pid):
    yield Metric(momentary_cpu_usage(pid), mem_top(pid)*100, number_of_children(pid))

def predict(pid, knn_model):
    df = pd.DataFrame(current_metrics(pid))
    return knn_model.predict(df)


