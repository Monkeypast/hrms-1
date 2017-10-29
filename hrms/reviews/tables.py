import django_tables2 as tables
from django.contrib.auth.models import User

class StaffTable(tables.Table):
    Peer_Review = tables.TemplateColumn('<a href="/reviews/wine/5">Review</a>')
    class Meta:
        model = User
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue','width':'100%', 'border': 1 }
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'date_joined')