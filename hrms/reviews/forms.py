from django.forms import ModelForm, Textarea
from reviews.models import Review, EmpReview


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
        }

class EmpReviewForm(ModelForm):
    class Meta:
        model = EmpReview
        fields = ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company', 'Work_accident', 'left', 'promotion_last_5years', 'department', 
                'salary', 'user_name']
#         widgets = {
#             'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
#         }