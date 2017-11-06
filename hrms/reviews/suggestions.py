from .models import Review, Wine, Cluster, EmpReview

from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, confusion_matrix, precision_recall_curve
from sklearn.preprocessing import RobustScaler
from .models import Review, Wine, Cluster, EmpReview, EmpPossibleResigneeReview
from django_pandas.io import read_frame

def update_clusters():
    num_reviews = Review.objects.count()
    update_step = ((num_reviews/100)+1) * 5
    if num_reviews % update_step == 0: # using some magic numbers here, sorry...
        # Create a sparse matrix from user reviews
        all_user_names = map(lambda x: x.username, User.objects.only("username"))
        all_wine_ids = set(map(lambda x: x.wine.id, Review.objects.only("wine")))
        num_users = len(all_user_names)
        ratings_m = dok_matrix((num_users, max(all_wine_ids)+1), dtype=np.float32)
        for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
            user_reviews = Review.objects.filter(user_name=all_user_names[i])
            for user_review in user_reviews:
                ratings_m[i,user_review.wine.id] = user_review.rating


        # Perform kmeans clustering
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())
        
        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before refering to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))
            

def save_resignee_from_row(resignee_row):
    resignee = EmpPossibleResigneeReview()
#     print(resignee_row['satisfaction'])
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
    #engine = create_engine('sqlite:///../db.sqlite3')
    #print(engine.has_table('reviews_empreview'))
    #df = pd.read_sql_table('reviews_empreview', engine)
    qs = EmpReview.objects.all()
    df = read_frame(qs)
    df.drop(df.columns[[0,1,12,13]],axis=1, inplace=True)

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
    df['department'].replace(['sales', 'accounting', 'hr', 'technical', 'support', 'management',
        'IT', 'product_mng', 'marketing', 'RandD'], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], inplace = True)
    df['salary'].replace(['LOW', 'MEDIUM', 'HIGH'], [0, 1, 2], inplace = True)
    df['turnover'].replace(['NO', 'YES'], [0, 1], inplace = True)
    df['workAccident'].replace(['NO', 'YES'], [0, 1], inplace = True)
    df['promotion'].replace(['NO', 'YES'], [0, 1], inplace = True)
    
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

    EmpPossibleResigneeReview.objects.all().delete()
#     for resignee in data_out.count(axis=0)
#         reg = EmpPossibleResigneeReview()
#         reg.id = resignee[0]
#         reg.satisfaction = resignee[1]
#         reg.evaluation = resignee[2]
#         reg.projectCount = resignee[3]
#         reg.averageMonthlyHours = resignee[4]
#         reg.yearsAtCompany = resignee[5]
#         reg.workAccident = resignee[6]
#         reg.promotion = resignee[7]
#         reg.department = resignee[8]
#         reg.salary = resignee[9]
#         reg.turnover = resignee[10]
#         reg.save()
        
#     new_possible_resignee = {i: EmpPossibleResigneeReview(name=i) for i in range(k)}
#     for cluster in new_possible_resignee.values(): # clusters need to be saved before refering to users
#         cluster.save()
#     for i,cluster_label in enumerate(clustering.labels_):
#         new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))
    #data_out.index.name = 'id'
    data_out.reset_index(level=0, inplace=True)
    #data_out['id'] = data_out.index
    print(data_out)
    data_out.apply(
        save_resignee_from_row,
        axis=1
    )
    #data_out.to_sql('reviews_emppossibleresigneereview',engine, if_exists='replace', index=True, index_label='id')
    