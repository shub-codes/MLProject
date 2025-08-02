# to hold code to transform the data
import sys
import os
from src.utils import save_object
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer 

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.custom_exception import CustomException
from src.logger import logging
'''
check notebook to learn about column transformer
Imputer is used to fill missing values
'''
'''
Pipeline Allows chaining multiple preprocessing steps and a model into one object.It ensures clean and reproducible workflows
PIPELINE- MLflow, KubeFlow, Airflow (for large-scale orchestration)

Typical Pipeline structure
[Data Collection]
       ↓
[Data Cleaning & Preprocessing]
       ↓
[Feature Engineering]
       ↓
[Model Training]
       ↓
[Model Evaluation]
       ↓
[Model Deployment (optional)]

'''
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    # this function will transform data
    def get_data_transformer_object(self):
        try:
            numerical_columns=['writing_score','reading_score']
            categorical_columns=['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']
            num_pipeline=Pipeline(
                # median is used because there are lot of outliers
                steps=[
                        ('imputer',SimpleImputer(strategy='median')),
                        ('scaler',StandardScaler())
                        ]

            )
            logging.info("Numerical Columns preprocessing completed")
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore')),
                    ('scaler', StandardScaler(with_mean=False)) 
                ]       
            )

            logging.info("Categiorical Columns preprocessing completed")
            logging.info(f"categorical columns: {categorical_columns}")
            logging.info(f"numerical columns: {numerical_columns}")

            # combining both pipelines into one
            preprocessor=ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Train and test data read intoo data transformer")
            logging.info("Obtaining pre processing object")
            preprocessing_obj=self.get_data_transformer_object()
            target_column_name="math_score"
            numerical_columns=['writing_score','reading_score']
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            logging.info("applying preprocessing object on training and testing dataframe")
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            #IMPORTANT: There is a difference between fit_transform and Transform
            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            logging.info("saving preprocessed object")
            # preprocessing_obj is created as a pickle fileand needs to be saved as such.
            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path, obj=preprocessing_obj)
            return(
                train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)
