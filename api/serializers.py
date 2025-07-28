from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema_field

class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ListUserSerializer(serializers.Serializer):
    user = GetUserSerializer(many=True)

class PutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_active']



    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

        request = self.context.get('request')
        if request:
            if request.method == 'GET':
                self.fields.pop('password', None)

            if request.method == 'PUT':
                self.fields.pop('id', None)
                self.fields.pop('username')
                self.fields.pop('password')

            if request.method == 'POST':
                self.fields.pop('is_active', None)

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

class CourseBundleAndPriceSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = CourseBundle
        fields = '__all__'

class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class GetBundlePriceSerializer():
    class Meta:
        model = BundlePrice

class ListCompanyCoursesAndStudentsForCompanySerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @extend_schema_field(GetUserSerializer(many=True))
    def get_students(self, obj):
        user_courses = obj.user_course_course.all()
        return GetUserSerializer([uc.user for uc in user_courses], many=True).data
    
class GetCompanyInfoWithSubsCountAndCurrentCountSerializer(serializers.ModelSerializer):
    totalSubscription = serializers.SerializerMethodField()
    currentCount = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_totalSubscription(self,obj):
        companySubs = obj.company_course_bundle_company.filter().latest('dateTime').totalCourseAmount
        return companySubs

    def get_currentCount(self, obj):
        currentCount = obj.course_to_company.filter().latest('courseDateTime').courseCount
        return currentCount
