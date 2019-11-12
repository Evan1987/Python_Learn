
"""
Use sklearn api
"""

import xlearn as xl
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score


data = load_iris()
X = data["data"]
y = data["target"] == 2


if __name__ == '__main__':
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    lr = xl.LRModel(task="binary", init=0.1, epoch=10, lr=0.1, reg_lambda=1.0, opt="sgd")
    lr.fit(X_train, y_train, eval_set=[X_test, y_test], is_lock_free=False)
    y_score = lr.predict(X_test)
    y_pred = y_score >= 0.5
    auc = roc_auc_score(y_test, y_score)
    acc = accuracy_score(y_test, y_pred)
    print(f"Auc.: {auc}, Acc.: {acc}")
