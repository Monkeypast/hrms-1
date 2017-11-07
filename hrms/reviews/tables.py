import django_tables2 as tables
from django.contrib.auth.models import User
from django_tables2 import A


class StaffTable(tables.Table):
    Peer_Review = tables.LinkColumn('reviews:staff_detail', text='Review', args=[A('pk')])

    # Peer_Review = tables.TemplateColumn('<a href="/reviews/wine/5">Review</a>')
    # Peer_Review = tables.TemplateColumn('<a href="{% url 'reviews:wine_detail' wine.id %}">Review</a>')
    class Meta:
        model = User
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue', 'width': '100%', 'border': 1}

        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined')


class PossibleResigneeTable(tables.Table):
    class Meta:
        model = User
        attrs = {'class': 'paleblue', 'width': '100%', 'border': 1}
        fields = ('id', 'satisfaction', 'evaluation', 'projectCount', 'yearsAtCompany', 'turnover')

class ReviewedEmployeeTable(tables.Table):
    class Meta:
        model = User
        attrs = {'class': 'paleblue', 'width': '100%', 'border': 1}
        fields = ('satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company', 'Work_accident',
                  'left', 'promotion_last_5years', 'department', 'salary', 'user_name', 'review_date')