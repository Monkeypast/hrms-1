from django.forms import ModelForm
from reviews.models import EmpReview

class EmpReviewForm(ModelForm):
    class Meta:
        model = EmpReview
        fields = ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company', 'Work_accident', 'left', 'promotion_last_5years', 'department', 
                'salary', 'review_date']
        labels = {
            'satisfaction_level': 'Satisfaction level'
        }