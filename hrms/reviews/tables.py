import django_tables2 as tables
from django.contrib.auth.models import User
from django_tables2 import A


class StaffTable(tables.Table):
    Peer_Review = tables.LinkColumn('reviews:staff_detail', text='Review', args=[A('pk')])

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
        fields = (
            'satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company',
            'Work_accident', 'promotion_last_5years', 'department', 'salary', 'staff', 'review_date')
