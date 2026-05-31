import os
import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
import pandas as pd
from dotenv import load_dotenv
import pymysql

import pickle
import numpy as np
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

load_dotenv()

host=os.getenv("host")
user=os.getenv("user")
passward=os.getenv("passward")
db=os.getenv("db")


def read_sql_data():
    logging.info("Reading sql database started")
    try:
        mydb=pymysql.connect(
            host=host,
            user=user,
            password=passward,
            db=db
        )
        logging.info("Connection established",mydb)
        df=pd.read_sql_query('Select * from students', mydb)
        print(df.head())

        return df

    except Exception as e:
        raise CustomException(e, sys)
    
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for model_name, model in models.items():
            para = param.get(model_name, {})

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            # Store raw float values, do not use np.round() without decimals
            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)