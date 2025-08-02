# code that handles ingestion(input of)
import sys
import os
from src.utils import save_object
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# import src.custom_exception
# importing sys and os touse our custom exceptions
from src.custom_exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass 
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
# https://docs.python.org/3/library/dataclasses.html
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join("artifacts","train.csv")
    test_data_path: str=os.path.join("artifacts","test.csv")
    raw_data_path: str=os.path.join("artifacts","raw.csv")
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        # when the class is called, the three variables of data ingestion config are storedin this class variable
    def initiate_data_ingestion(self):
        # to read the data from dataset/db
        logging.info("entering data ingestion method/component")
        try:
            df=pd.read_csv(r"C:\Users\HP\Desktop\Python\e2e MLProject\Notebook1\data\stud.csv")
            # can change path here to read from any source, ex mongodb, cockroachdb etc
            logging.info("reading dataset at dataframe")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            # os.path.dirname(self.ingestion_config.train_data_path) extracts the directory path (without the file name).
            # os.makedirs(..., exist_ok=True) creates the directory (and any intermediate ones) only if it doesn't already exist.
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            '''
                saves the DataFrame df to a CSV file at the path specified by self.ingestion_config.raw_data_path.
                index=False: prevents pandas from writing row numbers (indices) into the CSV.
                header=True: includes column names as the first row in the file (default behavior, but explicitly stated here).
            '''
            train_set,test_set=train_test_split(df,test_size=0.2, random_state=40)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("Data ingestion complete")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.error("Exception occurred in data ingestion", exc_info=True)
            raise CustomException(e,sys)
# testing the code
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    train_arr,test_arr,file_path=data_transformation.initiate_data_transformation(train_data,test_data)

    # last , left empty as we dont need the third returned value for current task
    modeltrainer=ModelTrainer()
    modeltrainer.initiate_model_trainer(train_arr,test_arr)