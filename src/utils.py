# utils is used to save common functions and functionalities that the wholeproject is going to use
import os
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from src.custom_exception import CustomException
def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)

def evaluate_model(x_train,y_train,x_test,y_test,models):
    try:
        report={}
        for model_key,model_val in models.items():
            model_val.fit(x_train,y_train)
            y_train_pred=model_val.predict(x_train)
            y_test_pred=model_val.predict(x_test)
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            report[model_key]=test_model_score
        return report
            

    except Exception as e:
        raise CustomException(e,sys)
