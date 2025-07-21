from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

'''
class LogTransactionSerializer(serializers.Serializer):
    log = models.JSONField()
'''

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = '__all__'
    
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = '__all__'

class CourseBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseBundle
        fields = '__all__'

class BundlePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundlePrice
        fields = '__all__'

class CompanyCourseBundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCourseBundle
        fields = '__all__'

class CourseBundleAndPrice(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = CourseBundle
        fields = '__all__'