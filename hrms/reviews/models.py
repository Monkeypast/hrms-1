from django.db import models
from django.contrib.auth.models import User
import numpy as np


class Wine(models.Model):
    name = models.CharField(max_length=200)
    
    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)
        
    def __unicode__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    wine = models.ForeignKey(Wine)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)

class EmpReview(models.Model):
    SALARY_CHOICES = (
        (0, 'LOW'),
        (1, 'MEDIUM'),
        (2, 'HIGH'),
    )
    WORK_ACCIDENT_CHOICES = (
        (0, 'NO'),
        (1, 'YES'),
    )
    LEFT_CHOICES = (
        (0, 'NO'),
        (1, 'YES'),
    )
    PROMOTION_CHOICES = (
        (0, 'NO'),
        (1, 'YES'),
    )
    DEPARTMENT_CHOICES = (
        (0, 'sales'),
        (1, 'accounting'),
        (2, 'hr'),
        (3, 'technical'),
        (4, 'support'),
        (5, 'management'),
        (6, 'IT'),
        (7, 'product_mng'),
        (8, 'marketing'),
        (9, 'RandD'),
    )
    staff = models.ForeignKey(User)
    satisfaction_level = models.DecimalField(max_digits=3, decimal_places=2)
    last_evaluation = models.DecimalField(max_digits=3, decimal_places=2)
    number_project = models.IntegerField()
    average_montly_hours = models.IntegerField()
    time_spend_company = models.IntegerField()
    Work_accident = models.IntegerField(choices=WORK_ACCIDENT_CHOICES)
    left = models.IntegerField(choices=LEFT_CHOICES)
    promotion_last_5years = models.IntegerField(choices=PROMOTION_CHOICES)
    department =models.IntegerField(choices=DEPARTMENT_CHOICES)
    salary = models.IntegerField(choices=SALARY_CHOICES)
    user_name = models.CharField(max_length=100)
    review_date = models.DateField()

class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])
