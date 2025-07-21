from django.shortcuts import render
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction as db_transaction
from .serializers import *

class UserViewSets(viewsets.ViewSet):
    def create(self, request):
        data = request.data.copy()
        data['is_active'] = True
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializers.ValidationError({'Something missing.'})

    def list(self, request):
        #permission_classes = [IsAuthenticated]
        user_header = request.user
        user_exist = check_user_exist_in_company(user_header)
        if user_exist:
            company = user_exist.company.pk
            list_user = UserCompany.objects.filter(company = company)
            for user in list_user:
                return
            serializer = UserSerializer(list_user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError('No users.')

    def retrieve(self, request, pk):
        user_header = request.user
        if user_header == pk:
            user = User.objects.get(pk = pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError('Not authorized.')

    def update(self, request, pk):
        #will be use
        return

def get_company_instance(user):
    company = Company.objects.get()
    return

# Create your views here.
class CourseBundleViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data.copy()
        user_header = request.user
        user_exist = check_user_superuser(user_header)
        if user_exist:
            course_price = data['price']
            data['user'] = user_header
            bundle_price_object = {}
            bundle_price_object.update({'price': course_price})
            course_bundle_serializer = CourseBundleSerializer(data=data)
            if course_bundle_serializer.is_valid():
                course_bundle_instance = course_bundle_serializer.save()

                bundle_price_object.update({'courseBundle': course_bundle_instance.pk})
                bundle_price_serializer = BundlePriceSerializer(data=bundle_price_object)
                if bundle_price_serializer.is_valid():
                    bundle_price_serializer.save()
                    return Response({'Response: Successful.'}, status=status.HTTP_200_OK)
                else: raise serializers.ValidationError('Few data missing.')
        
        else: raise serializers.ValidationError('Not authorized.')

    def list(self, request):
        list_course_bundle = CourseBundle.objects.filter(is_active =True)
        for single_course_price in list_course_bundle:
            bundle_price = BundlePrice.objects.filter(courseBundle =single_course_price.id).order_by('-dateTime').values('price').first()
            single_course_price.price = bundle_price['price']
        serializer = CourseBundleAndPrice(list_course_bundle, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        user = check_user_superuser()
        if user:
            course_bundle = CourseBundle.objects.get(pk = pk)
            serializer = CourseBundleSerializer(course_bundle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError('Not authorized.')

    def update(self, request, pk):
        #is only for is_active
        return

def check_company_course_count():
    return

class CompanyViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data.copy()
        user_header = request.user
        user_exist = check_user_exist_in_company(user_header)
        if user_exist:
            data['user'] = user_header
            company_serializer = CompanySerializer(data=data)
            if company_serializer.is_valid():
                company_instance = company_serializer.save()
                user_company_obj = {
                    "user" : user_header,
                    "company" : company_instance.instance.pk
                }
                user_company_serializer = UserCompanySerializer(data=user_company_obj)
                if user_company_serializer.is_valid():
                    user_company_serializer.save
                    return Response({'Success.'}, status=status.HTTP_200_OK)
                raise serializers.ValidationError('Something missing.')
            return serializers.ValidationError({'Something missing.'})
        else: raise serializers.ValidationError('Not authorized.')

    def list(self, request):
        return

    def retrieve(self, request, pk):
        user_header = request.user
        user_exist = check_user_exist_in_company(user_header)
        if user_exist:
            company = get_company_instance_through_user_company()
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError('No company.')

    def update(self, request, pk):
        #only for bank acct
        return

def get_company_instance_through_user_company(user):
    return UserCompany.objects.get(user = user).company

class UserCompanyViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data

        serializer = UserCompanySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializers.ValidationError({'Something missing.'})

    def list(self, request):
        return
    
    def retrieve(self, request, pk):
        return
    
    def update(self, request, pk):
        return
    

class CourseViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data

        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializers.ValidationError({'Something missing.'})

    def list(self, request):
        user_header = request.user
        user_exist = check_user_exist_in_company()
        if user_exist:
            company = UserCompany.objects.get(user = user_header).company.pk
            courses = list_course_for_company_only_courses(company)
        else: 
            courses = list_course_available()
        serializer = CourseSerializer(data=courses, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        retrieve_for_company_include_student()
        return
    
    def update(self, request, pk):
        return

def list_course_for_company_only_courses(company):
    try:
        courses = Course.objects.filter(company = company)
        return courses
    except: serializers.ValidationError('No courses made yet.')

def retrieve_for_company_include_student():
    return

def list_course_available():
    return Course.objects.filter(courseDateTime__gte = timezone.now())

class UserCourseViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data.copy()
        user_header = request.user
        data['user'] = user_header
        serializer = UserCourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializers.ValidationError({'Something missing.'})

    def list(self, request):
        return
    
    def retrieve(self, request, pk):
        return
    
    def update(self, request, pk):
        return

class BundlePriceViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data

        serializer = BundlePriceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializers.ValidationError({'Something missing.'})

    def list(self, request):
        return
    
    def retrieve(self, request, pk):
        return
    
    def update(self, request, pk):
        return

class CompanyCourseBundleViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data

        serializer = CompanyCourseBundleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return serializers.ValidationError({'Something missing.'})

    def list(self, request):
        return
    
    def retrieve(self, request, pk):
        return
    
    def update(self, request, pk):
        return

def check_user_exist_in_company(user):
    try:
        UserCompany.objects.get(user = user)
        return True
    except:
        return False

def user_from_auth():
    return

def user_from_body():
    return

def user_company():
    return

def user_user_company():
    return

def user_detail():
    return

def get_user_instance_from_company_pk():
    return

def check_user_admin():
    return

def check_user_superuser(user):
    return User.objects.get(user).is_superuser