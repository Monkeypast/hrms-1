from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),

    url(r'^staff$', views.staff_list, name='staff_list'),
    url(r'^predictedList$', views.predicted_list, name='predicted_list'),
    url(r'^empReviewedList', views.reviewed_list, name='reviewed_list'),
    url(r'^staff/(?P<staff_id>[0-9]+)/$', views.staff_detail, name='staff_detail'),
    url(r'^staff/(?P<staff_id>[0-9]+)/add_emp_review/$', views.add_emp_review, name='add_emp_review'),
    url(r'^emprecommendation/$', views.emp_recommendation_list, name='emp_recommendation_list'),
]
