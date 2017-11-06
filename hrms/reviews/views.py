from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Review, Wine, Cluster, EmpReview, EmpPossibleResigneeReview
from .forms import ReviewForm, EmpReviewForm
from .suggestions import update_clusters, train_Algorithm
from .tables import StaffTable
from django_tables2 import RequestConfig

from registration.backends.simple.views import RegistrationView

import datetime

from django.contrib.auth.decorators import login_required

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    context = {'wine_list':wine_list}
    return render(request, 'reviews/wine_list.html', context)

def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

@login_required
def staff_list(request):
    staff_list = StaffTable(User.objects.all())
    RequestConfig(request).configure(staff_list)
    return render(request, 'reviews/staff_list.html', {'staff_list': staff_list})
    #staff_list = User.objects.order_by('-username')
    #context = {'staff_list':staff_list}
    #return render(request, 'reviews/staff_list.html', context)
    
    #staff_list = User.objects.all()
    #return render(request, 'reviews/staff_list.html', {'staff_list': staff_list})

def staff_detail(request, staff_id):
    staff = get_object_or_404(User, pk=staff_id)
    form = EmpReviewForm()
    return render(request, 'reviews/staff_detail.html', {'staff': staff, 'form': form})

@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))
    
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

@login_required
def add_emp_review(request, staff_id):
    staff = get_object_or_404(User, pk=staff_id)
    form = EmpReviewForm(request.POST)
    if form.is_valid():
        #rating = form.cleaned_data['rating']
        #comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = EmpReview()
        review.staff = staff
        review.satisfaction_level = form.cleaned_data['satisfaction_level']
        review.last_evaluation = form.cleaned_data['last_evaluation']
        review.number_project = form.cleaned_data['number_project']
        review.average_montly_hours = form.cleaned_data['average_montly_hours']
        review.time_spend_company = form.cleaned_data['time_spend_company']
        review.Work_accident = form.cleaned_data['Work_accident']
        review.left = form.cleaned_data['left']
        review.promotion_last_5years = form.cleaned_data['promotion_last_5years']
        review.department = form.cleaned_data['department']
        review.salary = form.cleaned_data['salary']
        review.user_name = user_name
        review.review_date = form.cleaned_data['review_date']
        review.save()
        #update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:staff_detail', args=(staff.id,)))
    
    return render(request, 'reviews/staff_detail.html', {'staff': staff, 'form': form})

@login_required
def emp_recommendation_list(request):
    
    train_Algorithm()
    # get reviews from EmpPossibleResigneeReview
    emp_possible_resignee_review = EmpPossibleResigneeReview.objects.all()
    emp_possible_resignee_review_id = set(map(lambda x: x.id, emp_possible_resignee_review))
    
    emp_review = EmpReview.objects.filter(id__in=emp_possible_resignee_review_id)
    emp_review_user_name = set(map(lambda x: x.user_name, emp_review))
    
    # Get possible resignee list
    staff_list = StaffTable(User.objects.filter(username__in=emp_review_user_name))
    RequestConfig(request).configure(staff_list)
    return render(
        request, 
        'reviews/staff_recommendation_list.html', 
        {'username': request.user.username,'staff_list': staff_list}
    )
    

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    
    # get request user reviewed wines
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wine')
    user_reviews_wine_ids = set(map(lambda x: x.wine.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    
    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding wines reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(wine__id__in=user_reviews_wine_ids)
    other_users_reviews_wine_ids = set(map(lambda x: x.wine.id, other_users_reviews))
    
    # then get a wine list including the previous IDs, order by rating
    wine_list = sorted(
        list(Wine.objects.filter(id__in=other_users_reviews_wine_ids)), 
        key=lambda x: x.average_rating(), 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'wine_list': wine_list}
    )


class HRMSRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return "reviews/staff"
