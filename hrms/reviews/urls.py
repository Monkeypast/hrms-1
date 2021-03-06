from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /wine/
    url(r'^wine$', views.wine_list, name='wine_list'),

    url(r'^staff$', views.staff_list, name='staff_list'),
    url(r'^predictedList$', views.predicted_list, name='predicted_list'),
    url(r'^empReviewedList', views.reviewed_list, name='reviewed_list'),
    url(r'^staff/(?P<staff_id>[0-9]+)/$', views.staff_detail, name='staff_detail'),
    url(r'^staff/(?P<staff_id>[0-9]+)/add_emp_review/$', views.add_emp_review, name='add_emp_review'),
    url(r'^emprecommendation/$', views.emp_recommendation_list, name='emp_recommendation_list'),

    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail'),
    url(r'^wine/(?P<wine_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    # ex: /review/user - get reviews for the logged user
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    # ex: /review/user - get reviews for the user passed in the url
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    # ex: /recommendation - get wine recommendations for the logged user
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]
