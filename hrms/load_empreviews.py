import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hrms.settings")

import django
django.setup()

from reviews.models import EmpReview


def save_emp_review_from_row(review_row):
    review = EmpReview()
    review.id = review_row[0]
    review.satisfaction_level = review_row[1]
    review.last_evaluation = review_row[2]
    review.number_project = review_row[3]
    review.average_montly_hours = review_row[4]
    review.time_spend_company = review_row[5]
    review.Work_accident = review_row[6]
    review.left = review_row[7]
    review.promotion_last_5years = review_row[8]
    
    if review_row[9] == 'sales':
        review.department = 0
    elif review_row[9] == 'accounting':
        review.department = 1
    elif review_row[9] == 'hr':
        review.department = 2
    elif review_row[9] == 'technical':
        review.department = 3
    elif review_row[9] == 'support':
        review.department = 4
    elif review_row[9] == 'management':
        review.department = 5
    elif review_row[9] == 'IT':
        review.department = 6
    elif review_row[9] == 'product_mng':
        review.department = 7
    elif review_row[9] == 'marketing':
        review.department = 8
    else:
        review.department = 9
    
    if review_row[10] == 'low':
        review.salary = 0
    elif review_row[10] == 'medium':
        review.salary = 1
    else:
        review.salary = 2
    
    review.user_name = review_row[11]
    review.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        reviews_df = pd.read_csv(sys.argv[1])
        print(reviews_df)

        reviews_df.apply(
            save_emp_review_from_row,
            axis=1
        )

        print("There are reviews in DB" + str(EmpReview.objects.count()))
        
    else:
        print("Please, provide Reviews file path")
