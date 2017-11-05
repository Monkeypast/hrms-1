import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, confusion_matrix, precision_recall_curve
from sklearn.preprocessing import RobustScaler


engine = create_engine('sqlite:///../db.sqlite3')

# df = pd.read_sql_table('reviews_empreview', engine)
# df.drop(df.columns[[0,11,12,13]],axis=1, inplace=True)
# df = df.rename(columns={'satisfaction_level': 'satisfaction', 
#                             'last_evaluation': 'evaluation',
#                             'number_project': 'projectCount',
#                             'average_montly_hours': 'averageMonthlyHours',
#                             'time_spend_company': 'yearsAtCompany',
#                             'Work_accident': 'workAccident',
#                             'promotion_last_5years': 'promotion',
#                             'left' : 'turnover'
#                             })
# target_name = 'turnover'
# X = df.drop('turnover', axis=1)
# y = df[target_name]
# 
# X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.15, random_state=123, stratify=y)
# classifier = RandomForestClassifier(n_estimators=1000, max_depth=None, min_samples_split=10, class_weight="balanced")
# classifier.fit(X_train, y_train)
# 
# X_current = df[df.turnover < 1]
# X_current = X_current.drop('turnover', axis=1)
# y_current = classifier.predict(X_current)
# 
# X_current['turnover'] = y_current
# 
# data_out = X_current[X_current.turnover > 0]
# print(data_out)
# #confusion_matrix = confusion_matrix(y_test,y_pred)
# #print('confusion_matrix={0}'.format(confusion_matrix))
# #print('Score={0}'.format(classifier.score(X_test,y_test)))
# #print(classification_report(y_test,y_pred))
# #print(list(df.columns))


# df = pd.read_sql_table('reviews_empreview', engine)
# df.drop(df.columns[[0,11,12,13]],axis=1, inplace=True)
# # Renaming certain columns for better readability
# df = df.rename(columns={'satisfaction_level': 'satisfaction', 
#                         'last_evaluation': 'evaluation',
#                         'number_project': 'projectCount',
#                         'average_montly_hours': 'averageMonthlyHours',
#                         'time_spend_company': 'yearsAtCompany',
#                         'Work_accident': 'workAccident',
#                         'promotion_last_5years': 'promotion',
#                         'left' : 'turnover'
#                         })
# 
# # Convert these variables into categorical variables
# #df["department"] = df["department"].astype('category').cat.codes
# #df["salary"] = df["salary"].astype('category').cat.codes
# 
# # Move the reponse variable "turnover" to the front of the table
# front = df['turnover']
# df.drop(labels=['turnover'], axis=1,inplace = True)
# df.insert(0, 'turnover', front)
# 
# # Create an intercept term for the logistic regression equation
# df['int'] = 1
# #indep_var = ['satisfaction', 'evaluation', 'yearsAtCompany', 'int', 'turnover']
# indep_var = ['satisfaction', 'evaluation', 'projectCount','averageMonthlyHours', 'yearsAtCompany','workAccident','promotion','department','salary', 'int', 'turnover']
# df = df[indep_var]
# 
# # Create train and test splits
# target_name = 'turnover'
# X = df.drop('turnover', axis=1)
# 
# y=df[target_name]
# X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.15, random_state=123, stratify=y)
# 
# classifier = RandomForestClassifier(n_estimators=1000, max_depth=None, min_samples_split=10, class_weight="balanced")
# classifier.fit(X, y)
# X_current = df[df.turnover < 1]
# X_current = X_current.drop('turnover', axis=1)
# y_current = classifier.predict(X_current)
# 
# X_current['turnover'] = y_current
# 
# data_out = X_current[X_current.turnover > 0]
# data_out = data_out.drop('int', axis=1)
# print(data_out)
# data_out.to_sql('reviews_emppossibleresigneereview',engine, if_exists='replace', index=True, index_label='id')







engine = create_engine('sqlite:///../db.sqlite3')
print(engine.has_table('reviews_empreview'))
df = pd.read_sql_table('reviews_empreview', engine)
df.drop(df.columns[[0,11,12,13]],axis=1, inplace=True)
# Renaming certain columns for better readability
df = df.rename(columns={'satisfaction_level': 'satisfaction', 
                        'last_evaluation': 'evaluation',
                        'number_project': 'projectCount',
                        'average_montly_hours': 'averageMonthlyHours',
                        'time_spend_company': 'yearsAtCompany',
                        'Work_accident': 'workAccident',
                        'promotion_last_5years': 'promotion',
                        'left' : 'turnover'
                        })

# Convert these variables into categorical variables
#df["department"] = df["department"].astype('category').cat.codes
#df["salary"] = df["salary"].astype('category').cat.codes

# Move the reponse variable "turnover" to the front of the table
front = df['turnover']
df.drop(labels=['turnover'], axis=1,inplace = True)
df.insert(0, 'turnover', front)

# Create an intercept term for the logistic regression equation
df['int'] = 1
#indep_var = ['satisfaction', 'evaluation', 'yearsAtCompany', 'int', 'turnover']
indep_var = ['satisfaction', 'evaluation', 'projectCount','averageMonthlyHours', 'yearsAtCompany','workAccident','promotion','department','salary', 'int', 'turnover']
df = df[indep_var]

# Create train and test splits
target_name = 'turnover'
X = df.drop('turnover', axis=1)

y=df[target_name]

classifier = RandomForestClassifier(n_estimators=1000, max_depth=None, min_samples_split=10, class_weight="balanced")
classifier.fit(X, y)
X_current = df[df.turnover < 1]
X_current = X_current.drop('turnover', axis=1)
y_current = classifier.predict(X_current)

X_current['turnover'] = y_current

data_out = X_current[X_current.turnover > 0]
data_out = data_out.drop('int', axis=1)
print(data_out)
data_out.to_sql('reviews_emppossibleresigneereview',engine, if_exists='replace', index=True, index_label='id')