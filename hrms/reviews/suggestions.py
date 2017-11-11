from sklearn.ensemble import AdaBoostClassifier
import pandas as pd
from reviews.models import  EmpReview, EmpPossibleResigneeReview
from django_pandas.io import read_frame

def save_resignee_from_row(resignee_row):
    resignee = EmpPossibleResigneeReview()
    resignee.id = resignee_row['index']
    resignee.satisfaction = resignee_row['satisfaction']
    resignee.evaluation = resignee_row['evaluation']
    resignee.projectCount = resignee_row['projectCount']
    resignee.averageMonthlyHours = resignee_row['averageMonthlyHours']
    resignee.yearsAtCompany = resignee_row['yearsAtCompany']
    resignee.workAccident = resignee_row['workAccident']
    resignee.promotion = resignee_row['promotion']
    resignee.department = resignee_row['department']
    resignee.salary = resignee_row['salary']
    resignee.turnover = resignee_row['turnover']
    resignee.save()
            
def train_Algorithm():
    url = "data/HR_comma_sep.csv"
    df_train = pd.read_csv(url)
    #Check if null
    df_train.isnull().any()
    
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
    df_train['department'].replace(['sales', 'accounting', 'hr', 'technical', 'support', 'management',
        'IT', 'product_mng', 'marketing', 'RandD'], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], inplace = True)
    df_train['salary'].replace(['low', 'medium', 'high'], [0, 1, 2], inplace = True)
    
    # Move the reponse variable "turnover" to the front of the table
    front = df_train['turnover']
    df_train.drop(labels=['turnover'], axis=1,inplace = True)
    df_train.insert(0, 'turnover', front)
    
    # Create an intercept term for the logistic regression equation
    df_train['int'] = 1
    indep_var = ['satisfaction', 'evaluation', 'projectCount','averageMonthlyHours', 'yearsAtCompany','workAccident','promotion','department','salary', 'int', 'turnover']
    df_train = df_train[indep_var]

    # Create X and y for Training
    target_name = 'turnover'
    X_train = df_train.drop('turnover', axis=1)
    y_train =df_train[target_name]
    
    classifier = AdaBoostClassifier(n_estimators=400, learning_rate=0.1)
    classifier.fit(X_train, y_train)
    
    #End of train
    
    
    #Load data to be predicted from database table
    qs = EmpReview.objects.all()
    df_predict = read_frame(qs)
    df_predict.drop(df_predict.columns[[0,1,12,13]],axis=1, inplace=True)

    # Renaming certain columns for better readability
    df_predict = df_predict.rename(columns={'satisfaction_level': 'satisfaction', 
                            'last_evaluation': 'evaluation',
                            'number_project': 'projectCount',
                            'average_montly_hours': 'averageMonthlyHours',
                            'time_spend_company': 'yearsAtCompany',
                            'Work_accident': 'workAccident',
                            'promotion_last_5years': 'promotion',
                            'left' : 'turnover'
                            })
    
    # Convert these variables into categorical variables
    df_predict['department'].replace(['sales', 'accounting', 'hr', 'technical', 'support', 'management',
        'IT', 'product_mng', 'marketing', 'RandD'], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], inplace = True)
    df_predict['salary'].replace(['LOW', 'MEDIUM', 'HIGH'], [0, 1, 2], inplace = True)
    df_predict['turnover'].replace(['NO', 'YES'], [0, 1], inplace = True)
    df_predict['workAccident'].replace(['NO', 'YES'], [0, 1], inplace = True)
    df_predict['promotion'].replace(['NO', 'YES'], [0, 1], inplace = True)
    
    # Move the reponse variable "turnover" to the front of the table
    front = df_predict['turnover']
    df_predict.drop(labels=['turnover'], axis=1,inplace = True)
    df_predict.insert(0, 'turnover', front)
    
    # Create an intercept term for the logistic regression equation
    df_predict['int'] = 1
    indep_var = ['satisfaction', 'evaluation', 'projectCount','averageMonthlyHours', 'yearsAtCompany','workAccident','promotion','department','salary', 'int', 'turnover']
    df_predict = df_predict[indep_var]

    # Create train and test splits
    target_name = 'turnover'
    X_predict = df_predict.drop('turnover', axis=1)
    y_predict =df_predict[target_name]

    y_current = classifier.predict(X_predict)
    X_predict['turnover'] = y_current
    
    data_out = X_predict
    data_out = data_out.drop('int', axis=1)

    EmpPossibleResigneeReview.objects.all().delete()
    data_out.reset_index(level=0, inplace=True)
    data_out.apply(
        save_resignee_from_row,
        axis=1
    )