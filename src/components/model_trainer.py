import sys
import os
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from  xgboost import XGBRegressor
from src.custom_exception import CustomException
from src.logger import logging
from src.utils import evaluate_model
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    trained_mode_file_path=os.path.join("artifacts","model.pkl")
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info("split train and test info")
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1]
            )
            models = {
            "Linear Regression": LinearRegression(),
            "K-Neighbors Regressor": KNeighborsRegressor(),
            "Decision Tree": DecisionTreeRegressor(),
            "Random Forest Regressor": RandomForestRegressor(),
            "XGBRegressor": XGBRegressor(), 
            "CatBoosting Regressor": CatBoostRegressor(verbose=False),
            "AdaBoost Regressor": AdaBoostRegressor(),
            "GradientBoosting":GradientBoostingRegressor()
            }
            # evaluate_model is a function created in utils
            model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)
            best_model_score=max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model=models[best_model_name]
            if best_model_score<0.6:
                raise CustomException("no model is efficient enough")
            logging.info(f"best model found {best_model_name} with score {best_model_score*100} %")

            save_object(file_path=self.model_trainer_config.trained_mode_file_path, obj=best_model)
            # now we will use best model to predict the x_test values
            predicted=best_model.predict(x_test)
            r2_square=r2_score(y_test,predicted)
            return r2_square

        except Exception as e:
            raise CustomException(e,sys)