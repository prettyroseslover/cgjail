from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.metrics import classification_report
from pathlib import Path
from joblib import dump
from metrics.memory import memtotal_bytes


def k_neigh(n):
    import numpy as np
    return int(np.ceil(np.sqrt(n) / 2.) * 2 + 1)


class Model:
    def __init__(self, input, path_to_storage, K=None):
        df = pd.read_csv(input)
        X = df.loc[:, df.columns!='process_class']
        y = df['process_class']
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(X, y, test_size = 0.2, random_state=0)
        self.K = k_neigh(len(self.y_train)) if K == None else K
        self.model_name = f"{path_to_storage}/{Path(input).stem}.pkl"
        self.kNN = None
        # prepare acceptable values for given model
        docile_behaviour = df.loc[df['process_class'] == 0]
        self.cpu_usage_quota = int(docile_behaviour['cpu_usage'].quantile(0.9) / 100 * 100000)
        self.mem_max_bytes = int(docile_behaviour['memory_usage'].quantile(0.9) / 100 * memtotal_bytes())
        self.maximum_number_of_processes = docile_behaviour['number_of_children'].max()

    def train_and_save(self):
        self.kNN = KNeighborsClassifier(n_neighbors = self.K, p = 1)
        self.kNN.fit(self.x_train, self.y_train)
        # add extra information
        self.kNN.cpu_usage_quota = self.cpu_usage_quota
        self.kNN.mem_max_bytes = self.mem_max_bytes
        self.kNN.maximum_number_of_processes = self.maximum_number_of_processes
        # save
        dump(self.kNN, self.model_name)

    def quality(self):
        predictions = self.kNN.predict(self.x_test)
        return classification_report(self.y_test, predictions)