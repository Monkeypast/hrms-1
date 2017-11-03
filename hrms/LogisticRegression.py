#####    IMPORT MODULES    #####
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
#from patsy import dmatrices
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, confusion_matrix, precision_recall_curve
import seaborn as sns
from sklearn.preprocessing import RobustScaler

#####    DATA-PREPROCESSING    #####
df = pd.read_csv('data/HR_comma_sep.csv')
df.drop(df.columns[[0,11]],axis=1, inplace=True)
#print(df.isnull().any())

# Convert "department" and "salary" features to numeric types because some functions won't be able to work with string types
df['department'].replace(['sales', 'accounting', 'hr', 'technical', 'support', 'management',
        'IT', 'product_mng', 'marketing', 'RandD'], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], inplace = True)
df['salary'].replace(['low', 'medium', 'high'], [0, 1, 2], inplace = True)

# Renaming certain columns for better readability
# df = df.rename(columns={'satisfaction_level': 'satisfaction', 
#                         'last_evaluation': 'evaluation',
#                         'number_project': 'projectCount',
#                         'average_montly_hours': 'averageMonthlyHours',
#                         'time_spend_company': 'yearsAtCompany',
#                         'Work_accident': 'workAccident',
#                         'promotion_last_5years': 'promotion',
#                         'department' : 'department',
#                         'left' : 'turnover'
#                         })

df["department"] = df["department"].astype('category').cat.codes
print(df["department"])
# Move the reponse variable "turnover" to the front of the table
front = df['turnover']
df.drop(labels=['turnover'], axis=1,inplace = True)
df.insert(0, 'turnover', front)
#print(df.head())
#turnover_rate = df.turnover.value_counts() / len(df)
#print(df.turnover.value_counts())
print(df.workAccident.value_counts())
print(df.groupby('turnover').mean())

#Correlation Matrix
corr = df.corr()
corr = (corr)
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
sns.plt.title('Heatmap of Correlation Matrix')
#plt.show()

#clarity_color_table = pd.crosstab(index=df["department"], columns=df["turnover"])
#clarity_color_table.plot(kind="bar", figsize=(5,5), stacked=True)
clarity_color_table = pd.crosstab(index=df["department"], 
                          columns=df["salary"])

clarity_color_table.plot(kind="bar", 
                 figsize=(5,5),
                 stacked=True)
plt.show()


