

import os
import xlearn as xl


data_path = r"F:\for learn\Python\Repo_sources\xlearn\demo\classification\criteo_ctr"
train_file = os.path.join(data_path, "small_train.txt")
test_file = os.path.join(data_path, "small_test.txt")
output_model = os.path.join(data_path, "temp.model")
output_file = os.path.join(data_path, "predict.txt")

# add additional params like:
# "fold": 3(default)
# "opt": "sgd", "adagrad"(default) or "ftrl"
# "lr": 0.2(default)
# "lambda": 0.0002(default)
# for ftrl, could pass other regularization: "alpha": 0.002, "beta": 0.8, "lambda_1": 0.001, "lambda_2": 1.0
# "k": 4(default),  the length of hidden vector for fm and ffm. As using SSE, the cost of time is equal for k=2 and k=4
# "init": 0.66(default),  initial param
# "epoch": 10, if have set validation set, the train will early stop at best validation result.
# "stop_window": 2, the window size for early-stop.
#                   If the validation result hasn't improved after $stop_window epoch, stop training.
# "metric": if not set, the metric for validation will be the loss itself.
# "nthread": int, default using all cpu cores to train lock-freely. which is non-deterministic.

param = {"task": "binary", "lr": 0.2, "lambda": 0.002, "metric": "acc"}


if __name__ == '__main__':
    ffm_model = xl.create_ffm()
    ffm_model.setTrain(train_file)
    ffm_model.setValidate(test_file)
    # ffm_model.setQuiet()  # not compute any metrics, will increase training efficiency significantly.
    # ffm_model.disableNorm()  # to disable instance-wised normalization
    # ffm_model.disableLockFree()  # to disable training on multi-threads, be deterministic.
    # ffm_model.disableEarlyStop()  # to disable early-stop
    # ffm_model.setOnDisk()  # whether calculate on disk to save memory
    ffm_model.setTXTModel(output_model)  # output model in txt, easy for human reading
    # ffm_model.setPreModel( #pre_byte_model_path)  # for online learning, only load model in bytes not in txt
    ffm_model.fit(param, output_model)
    # ffm_model.cv(param)  # do cv on given params, 3-fold by default, but could pass {"fold": 5} into param

    ffm_model.setTest(test_file)
    # ffm_model.setSigmoid()   # strict to (0, 1)
    ffm_model.setSign()  # return 0 or 1
    ffm_model.predict(output_model, output_file)
