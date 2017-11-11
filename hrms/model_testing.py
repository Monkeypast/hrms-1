#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 22:54:07 2017

@author: misitesawn
"""



from sklearn.ensemble import AdaBoostClassifier


import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, confusion_matrix, precision_recall_curve
from sklearn.preprocessing import RobustScaler
    # load dataset
    url = "data/HR_comma_sep.csv"
    #names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
    df_train = pd.read_csv(url)
    
    # Renaming certain columns for better readability
    df_train = df_train.rename(columns={'satisfaction_level': 'satisfaction', 
                            'last_evaluation': 'evaluation',
                            'number_project': 'projectCount',
                            'average_montly_hours': 'averageMonthlyHours',
                            'time_spend_company': 'yearsAtCompany',
                            'Work_accident': 'workAccident',
                            'promotion_last_5years': 'promotion',
                            'sales': 'department',
                            'left' : 'turnover'
                            })
    
    # Convert these variables into categorical variables
    #df["department"] = df["department"].astype('category').cat.codes
    #df["salary"] = df["salary"].astype('category').cat.codes
    df_train['department'].replace(['sales', 'accounting', 'hr', 'technical', 'support', 'management',
        'IT', 'product_mng', 'marketing', 'RandD'], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], inplace = True)
    df_train['salary'].replace(['low', 'medium', 'high'], [0, 1, 2], inplace = True)
    #df_train['turnover'].replace(['NO', 'YES'], [0, 1], inplace = True)
    #df_train['workAccident'].replace(['NO', 'YES'], [0, 1], inplace = True)
   # df_train['promotion'].replace(['NO', 'YES'], [0, 1], inplace = True)
    
    # Move the reponse variable "turnover" to the front of the table
    front = df_train['turnover']
    df_train.drop(labels=['turnover'], axis=1,inplace = True)
    df_train.insert(0, 'turnover', front)
    
    # Create an intercept term for the logistic regression equation
    df_train['int'] = 1
    #indep_var = ['satisfaction', 'evaluation', 'yearsAtCompany', 'int', 'turnover']
    indep_var = ['satisfaction', 'evaluation', 'projectCount','averageMonthlyHours', 'yearsAtCompany','workAccident','promotion','department','salary', 'int', 'turnover']
    df_train = df_train[indep_var]

    # Create train and test splits
    target_name = 'turnover'
    X = df_train.drop('turnover', axis=1)
    
    Y =df_train[target_name]
    #################
    
   
    
    X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size=0.33, random_state=42)
    
    # Spilt data into 
    
    clf = AdaBoostClassifier(n_estimators=400, learning_rate=0.1)
   
    clf.fit(X_train, y_train)
    
  
    
    #predict
    prediction  = clf.predict(X_test)
    #score
    print ('score:', clf.score(X_test, y_test))
    
     ## The line / model
    plt.scatter(y_test, predictions)
    plt.xlabel(â€œValuesâ€�)
    plt.ylabel(â€œPredictionsâ€�)
    
 


    
    
    
    