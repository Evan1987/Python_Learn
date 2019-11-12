
"""
Use DMatrix api to train and test
Cross-validation hasn't support DMatrix yet, but will do soon.
"""


import os
import xlearn as xl
import pandas as pd


data_path = r"F:\for learn\Python\Repo_sources\xlearn\demo\regression\house_price"
train_file = os.path.join(data_path, "house_price_train.txt")
test_file = os.path.join(data_path, "house_price_test.txt")
output_model = os.path.join(data_path, "temp.model")
output_file = os.path.join(data_path, "output.txt")
param = {"task": "reg", "lr": 0.2, "lambda": 0.002, "metric": "mae"}


if __name__ == '__main__':
    train_data = pd.read_csv(train_file, sep="\t", header=None)
    test_data = pd.read_csv(test_file, sep="\t", header=None)
    columns = train_data.columns
    X_train = train_data[columns[1:]]
    y_train = train_data[0]

    X_test = test_data[columns[1:]]
    y_test = test_data[0]

    train_matrix = xl.DMatrix(X_train, y_train)
    test_matrix = xl.DMatrix(X_test, y_test)

    fm_model = xl.create_fm()
    fm_model.setTrain(train_matrix)
    fm_model.setValidate(test_matrix)

    fm_model.fit(param, output_model)
    fm_model.setTest(test_matrix)

    fm_model.predict(output_model, output_file)

