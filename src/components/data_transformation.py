import sys
import os
from dataclasses import dataclass

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path= os.path.join('artifact',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_column=["reading_score","writing_score"]

            categorical_column=["gender",
                                "race_ethnicity",
                                "parental_level_of_education",
                                "lunch",
                                "test_preparation_course",
                                ]
            
            numerical_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            categorical_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Numerical pipeline implemented for: {numerical_column}")
            logging.info(f"Categorical pipeline implemented for:{categorical_column}")

            preprocessor=ColumnTransformer(
                [
                    ("numerical_pipeline",numerical_pipeline,numerical_column),
                    ("categorical_pipeline",categorical_pipeline,categorical_column)
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path, test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test done")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_column=["reading_score","writing_score"]

            input_train_feature_df=train_df.drop(columns=[target_column_name],axis=1)
            target_train_feature_df=train_df[target_column_name]

            input_test_feature_df=test_df.drop(columns=[target_column_name],axis=1)
            target_test_feature_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessor object on training and testing dataframes"
            )
            
            input_train_feature_arr= preprocessing_obj.fit_transform(input_train_feature_df)
            input_test_feature_arr= preprocessing_obj.transform(input_test_feature_df)


            train_arr = np.c_[
                input_train_feature_arr, np.array(target_train_feature_df)
            ]

            test_arr = np.c_[input_test_feature_arr, np.array(target_test_feature_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        
        except Exception as e:
            raise CustomException(e,sys)   
        

        
            


