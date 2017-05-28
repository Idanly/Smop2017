import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

balance_data = pd.read_csv(
    'https://archive.ics.uci.edu/ml/machine-learning-databases/balance-scale/balance-scale.data',
    sep=',', header=None)
DecisionTreeClassifier()