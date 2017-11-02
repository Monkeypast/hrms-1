from django.forms import ModelForm, Textarea
from reviews.models import Review, EmpReview

# class Slider(forms.RangeInput):
#     min = 5
#     max = 20
#     step = 5
#     template_name = 'slider.html'
# 
#     class Media:
#         js = (
#             'js/jquery.min.js',
#             'js/jquery-ui.min.js',
#         )
#         css = {
#             'all': (
#                 'css/jquery-ui.css',
#             )
#         }

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
        labels = {
#             'satisfaction_level': 'Satisfaction Level:',
            'Work_accident':'Work Accident',
        }
        widgets = {
#             'satisfaction_level': forms.RangeInput(attrs={'min': 0, 'max': 15}),
#             'user_name': Textarea(attrs={'cols': 40, 'rows': 15}),
        }