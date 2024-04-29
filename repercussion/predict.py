import sys
sys.path.insert(0, '../') # how to beautify that? 
from metrics.cpu import momentary_cpu_usage
from metrics.children import number_of_children
from metrics.memory import mem_top

def current_metrics(pid) -> (float, float, int):
    return (momentary_cpu_usage(pid), mem_top(pid)*100, number_of_children(pid))


def predict(pid, knn_model):
    return knn_model.predict([current_metrics(pid)])


