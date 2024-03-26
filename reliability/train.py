from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.metrics import classification_report
from pathlib import Path
from joblib import dump


def k_neigh(n):
    import numpy as np
    return int(np.ceil(np.sqrt(n) / 2.) * 2 + 1)


class Model:
    def __init__(self, input, path_to_storage, K=None):
        df = pd.read_csv(input, index_col = 0)
        X = df.loc[:, df.columns!='process_class']
        y = df['process_class']
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(X, y, test_size = 0.2, random_state=0)
        self.K = k_neigh(len(self.y_train)) if K == None else K
        self.model_name = f"{path_to_storage}/{Path(input).stem}.pkl"
        self.kNN = None

    def train_and_save(self):
        self.kNN = KNeighborsClassifier(n_neighbors = self.K, p = 1)
        self.kNN.fit(self.x_train, self.y_train)
        dump(self.kNN, self.model_name)

    def quality(self):
        predictions = self.kNN.predict(self.x_test)
        return classification_report(self.y_test, predictions)
