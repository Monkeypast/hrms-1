from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from .models import EmpReview, EmpPossibleResigneeReview
from .forms import EmpReviewForm
from .suggestions import train_Algorithm
from .tables import StaffTable, PossibleResigneeTable, ReviewedEmployeeTable
from django_tables2 import RequestConfig
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required


def review_list(request):
    return render(request, 'reviews/review_list.html')

@login_required
def staff_list(request):
    staff_list = StaffTable(User.objects.all())
    RequestConfig(request).configure(staff_list)
    return render(request, 'reviews/staff_list.html', {'staff_list': staff_list})

@login_required
def predicted_list(request):
    predicted_list = PossibleResigneeTable(EmpPossibleResigneeReview.objects.all())
    RequestConfig(request).configure(predicted_list)
    return render(request, 'reviews/predicted_list.html', {'predicted_list': predicted_list})

@login_required
def reviewed_list(request):
    reviewed_list = ReviewedEmployeeTable(EmpReview.objects.all())
    RequestConfig(request).configure(reviewed_list)
    return render(request, 'reviews/reviewed_list.html', {'reviewed_list': reviewed_list})

def staff_detail(request, staff_id):
    staff = get_object_or_404(User, pk=staff_id)
    form = EmpReviewForm()
    return render(request, 'reviews/staff_detail.html', {'staff': staff, 'form': form})

@login_required
def add_emp_review(request, staff_id):
    staff = get_object_or_404(User, pk=staff_id)
    form = EmpReviewForm(request.POST)
    if form.is_valid():
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

    reviewed_list = ReviewedEmployeeTable(EmpReview.objects.all())
    RequestConfig(request).configure(reviewed_list)
    return render(request, 'reviews/reviewed_list.html', {'reviewed_list': reviewed_list})


@login_required
def emp_recommendation_list(request):
    train_Algorithm()
    # predicted_list(request)
    predicted_list = PossibleResigneeTable(EmpPossibleResigneeReview.objects.all())
    RequestConfig(request).configure(predicted_list)
    return render(request, 'reviews/predicted_list.html', {'predicted_list': predicted_list})

class HRMSRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return "reviews/staff"
