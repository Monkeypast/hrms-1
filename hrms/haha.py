import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
from sklearn.metrics import confusion_matrix, classification_report

# data = pd.read_csv('banking.csv')
data = pd.read_csv('data/HR_comma_sep.csv')
print(data.describe())
print(data.shape)
print(list(data.columns))

# sns.countplot(y='job', data=data)
# plt.show()

# data.drop(data.columns[[0,3,7,8,9,10,11,12,13,15,16,17,18,19]],axis=1, inplace=True)
data.drop(data.columns[[0,11]],axis=1, inplace=True)
print(data.head())

# data2=pd.get_dummies(data, columns=['job','marital','default','housing','loan','poutcome'])
data2=pd.get_dummies(data, columns=['satisfaction_level','last_evaluation','number_project','average_montly_hours','time_spend_company','Work_accident', 'Work_accident','promotion_last_5years','department','salary','left'])
print(data2.head())

# data2.drop(data2.columns[[12,16,18,21,24]], axis=1, inplace=True)

sns.heatmap(data2.corr())
plt.show()



# X=data2.iloc[:,1:]
# y=data2.iloc[:,0]
# X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=0)
# 
# print(X_train.shape)
# 
# classifier = LogisticRegression(random_state=0)
# classifier.fit(X_train,y_train)
# 
# y_pred = classifier.predict(X_test)
# confusion_matrix = confusion_matrix(y_test,y_pred)
# print(confusion_matrix)
# 
# print(classifier.score(X_test,y_test))
# 
# print(classification_report(y_test,y_pred))
