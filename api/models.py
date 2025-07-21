from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class LogTransaction(models.Model):
    log = models.JSONField()

class Company(models.Model):
    name = models.CharField(max_length=100)
    bankName = models.CharField(max_length=100)
    bankAccount = models.CharField(max_length=100)

class UserCompany(models.Model):
    user = models.ForeignKey(User, related_name='user_company_user', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='user_company_company', on_delete=models.CASCADE)

class Course(models.Model):
    title = models.CharField(max_length=100)
    trainerName = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    courseDateTime = models.DateTimeField(default=timezone.now, blank=True)
    maxSeat = models.IntegerField()
    description = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    whatsappGroupLink = models.CharField(max_length=200)
    hideOnFull = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="course_to_company")
    is_active = models.BooleanField(default=True)
    hrdfClaimable = models.BooleanField()
    courseCount = models.IntegerField()

class UserCourse(models.Model):
    user = models.ForeignKey(User, related_name='user_course_user', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='user_course_course', on_delete=models.CASCADE)

class CourseBundle(models.Model):
    courseAmount = models.IntegerField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name='course_bundle_user', on_delete=models.CASCADE)

class BundlePrice(models.Model):
    courseBundle = models.ForeignKey(CourseBundle, related_name='bundle_price_course_bundle', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    dateTime = models.DateTimeField(default=timezone.now)

class CompanyCourseBundle(models.Model):
    company = models.ForeignKey(Company, related_name='company_course_bundle_company', on_delete=models.CASCADE)
    bundlePrice = models.ForeignKey(BundlePrice, related_name='company_course_bundle_bundle_price', on_delete=models.CASCADE)
    totalCourseAmount = models.IntegerField()
    dateTime = models.DateTimeField(default=timezone.now)