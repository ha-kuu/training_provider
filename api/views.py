from django.shortcuts import render
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction as db_transaction
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework.pagination import LimitOffsetPagination
from .swagger_text import *
from .drf_spec_open_api import *
from .drf_spec_msg_serializer import *

class UserViewSets(viewsets.ViewSet):
    @extend_schema(
            description=dsoa_post_user['description'],
            parameters=None,
            request= PostUserSerializer,
            responses={
                200:UserSerializer,
                400:OpenApiResponse(description="Data not valid.")
            }
    )
    def create(self, request):
        data = request.data.copy()
        data['is_active'] = True
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError('Data not valid.')

    @extend_schema(
            description=dsoa_list_user['description'],
            responses={
                200:GetUserSerializer(many=True),
                400:OpenApiResponse(description='Authentication credentials were not provided.'),
                401:OpenApiResponse(description='Not authorized.')
            }
    )
    def list(self, request):
        #permission_classes = [IsAuthenticated]
        user_header = request.user
        user_exist = check_user_exist_in_company(user_header)
        user_list = []
        if user_exist:
            company = UserCompany.objects.get(user = user_header.pk).company
            list_user_in_company = UserCompany.objects.filter(company = company).select_related('user')
            for user_obj in list_user_in_company:
                user_list.append(user_obj.user)
            serializer = GetUserSerializer(user_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError('Not authorized')

    @extend_schema(
            description=dsoa_retrieve_user['description'],
            responses={
                200:GetUserSerializer,
                400:OpenApiResponse(description='Not authorized.'),
                401:OpenApiResponse(description='Authentication credentials were not provided.'),
            }
    )
    def retrieve(self, request, pk):
        user_header = request.user
        if user_header.pk == int(pk):
            user = User.objects.get(pk = pk)
            serializer = GetUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError('Not authorized.')

    @extend_schema(
            exclude=True,
            request=PutUserSerializer
    )
    def update(self, request, pk):
        #will be use
        return

@extend_schema(exclude=True)
class CourseBundleViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data.copy()
        user_header = request.user
        if user_header.is_superuser:
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
            bundle_price = BundlePrice.objects.filter(courseBundle = single_course_price.id).order_by('-dateTime').values('price').first()
            single_course_price.price = bundle_price['price']
        serializer = CourseBundleAndPriceSerializer(list_course_bundle, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        user_header = request.user
        if user_header.is_superuser:
            course_bundle = CourseBundle.objects.get(pk = pk)
            serializer = CourseBundleSerializer(course_bundle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError('Not authorized.')

    @extend_schema(
            exclude=True
    )
    def update(self, request, pk):
        #is only for is_active
        return

class CompanyViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            description=dsoa_post_company['description'],
            parameters=None,
            request=CompanySerializer,
            responses={
                200:OpenApiResponse(description='Success.'),
                400:OpenApiResponse(description='Authentication credentials were not provided.'),
                401:OpenApiResponse(description='Not authorized.')
            }
    )
    def create(self, request):
        data = request.data.copy()
        name = data['name']
        check_company_name(name)
        user_header = request.user
        user_exist = check_user_exist_in_company(user_header)
        if not user_exist:
            company_serializer = CompanySerializer(data=data)
            if company_serializer.is_valid():
                company_instance = company_serializer.save()
                user_company_obj = {
                    "user" : user_header.pk,
                    "company" : company_instance.pk
                }
                user_company_serializer = UserCompanySerializer(data=user_company_obj)
                if user_company_serializer.is_valid():
                    user_company_serializer.save()
                    return Response({'Success.'}, status=status.HTTP_200_OK)
                raise serializers.ValidationError(user_company_serializer.errors)
            raise serializers.ValidationError(company_serializer.errors)
        else: raise serializers.ValidationError('Already in a company.')

    @extend_schema(
            description=dsoa_list_company['description'],
            responses={
                200:GetCompanyInfoWithSubsCountAndCurrentCountSerializer,
                400:OpenApiResponse(description='No company.')
                }
    )
    def list(self, request):
        user_header = request.user
        user_exist = check_user_exist_in_company(user_header)
        if user_exist:
            company = get_company_instance_through_user_company(user_header)
            serializer = GetCompanyInfoWithSubsCountAndCurrentCountSerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: raise serializers.ValidationError('No company.')

    @extend_schema(exclude=True)
    def retrieve(self, request, pk):
        user_header = request.user
        user_exist = check_user_exist_in_company(user_header)
        if user_exist:
            company = get_company_instance_through_user_company(user_header)
            serializer = GetCompanyInfoWithSubsCountAndCurrentCountSerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: raise serializers.ValidationError('No company.')

    @extend_schema(exclude=True)
    def update(self, request, pk):
        #only for bank acct
        return

@extend_schema(exclude=True)
class UserCompanyViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data

        serializer = UserCompanySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError(serializer.errors)

class CourseViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    @extend_schema(
            request=CourseSerializer,
            responses={
                200:CourseSerializer,
                400:OpenApiResponse(description='Not authorized.'),
                401:OpenApiResponse(description='Authentication credentials were not provided.'),
            }
    )
    def create(self, request):
        data = request.data.copy()
        user_header = request.user
        company = get_company_instance_through_user_company(user_header)
        company_course_count = get_course_count_through_company_course_bundle(company)
        if data['price'] < 1: return serializers.ValidationError('Price cant be lower than Rm1.')
        data['company'] = company.pk
        if company_course_count == None:
            raise serializers.ValidationError('Company have not bought any subscriptions.')
        current_course_count = get_last_course_count_through_latest_course(company)
        if company_course_count <= current_course_count :
            raise serializers.ValidationError('Max count reached.')
        data['courseCount'] = current_course_count + 1
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError(serializer.errors)

    @extend_schema(
            request=CourseSerializer,
            parameters=[
                OpenApiParameter(name='limit', type=int, location=OpenApiParameter.QUERY, description='Number of items per page'),
                OpenApiParameter(name='offset', type=int, location=OpenApiParameter.QUERY, description='Starting index of results'),
    ],
            responses={
                200:ListCompanyCoursesAndStudentsForCompanySerializer,
                400:OpenApiResponse(description='Not authorized.'),
                401:OpenApiResponse(description='Authentication credentials were not provided.'),
            },
    )
    def list(self, request):
        user_header = request.user
        user_exist = check_user_exist_in_company(user_header)
        if user_exist:
            company = UserCompany.objects.get(user = user_header).company.pk
            courses = list_course_for_company_only_courses(company)
        else: 
            courses = list_course_available()
        paginator = LimitOffsetPagination()
        paginated_qs = paginator.paginate_queryset(courses, request)

        # Serialize
        serializer = ListCompanyCoursesAndStudentsForCompanySerializer(
            paginated_qs, many=True
        )
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
            description=dsoa_retrieve_course['description'],
            responses=CourseSerializer
    )
    def retrieve(self, request, pk):
        course = Course.objects.get(pk = pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
            exclude=True
    )
    def update(self, request, pk):
        return

def check_company_course_count(company_count, current_course_count):
    if company_count >= current_course_count:
        return True
    return False

def list_course_for_company_only_courses(company):
    courses = Course.objects.filter(company=company).prefetch_related(
        'user_course_course__user'
    )
    if not courses.exists():
        # Raise the error correctly
        raise serializers.ValidationError('No courses made yet.')
    return courses

def retrieve_for_company_include_student():
    return

def list_course_available():
    try:
        return Course.objects.filter(courseDateTime__gte = timezone.now())
    except: raise serializers.ValidationError({'Something missing.'})

class UserCourseViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data.copy()
        user_header = request.user
        data['user'] = user_header.pk
        serializer = UserCourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError(serializer.errors)

@extend_schema(exclude=True)
class BundlePriceViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def create(self, request):
        data = request.data

        serializer = BundlePriceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError({'Something missing.'})

class CompanyCourseBundleViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            request=CompanyCourseBundleSerializer,
            responses={
                200:CompanyCourseBundleSerializer,
                400:OpenApiResponse(description='Authentication credentials were not provided.'),
                401:OpenApiResponse(description='Not authorized.')
            }    
    )
    def create(self, request):
        data = request.data.copy()
        user_header = request.user
        company = get_company_instance_through_user_company(user_header)
        company_course_count = get_course_count_through_company_course_bundle(company)
        bundle = data['bundlePrice']
        course_bundle_count = get_course_count_through_bundle_price(bundle)
        data['company'] = company.pk
        if company_course_count == None:
            data['totalCourseAmount'] = course_bundle_count
        else: data['totalCourseAmount'] = company_course_count + course_bundle_count
        serializer = CompanyCourseBundleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise serializers.ValidationError(serializer.errors)

    @extend_schema(
            exclude=True
    )
    def list():
        return

    @extend_schema(
            exclude=True
    )
    def retrieve():
        return

    @extend_schema(
            exclude=True
    )
    def update():
        return

def check_user_exist_in_company(user):
    try:
        UserCompany.objects.get(user = user)
        return True
    except:
        return False

def get_course_count_through_company_course_bundle(company):
    try:
        return CompanyCourseBundle.objects.filter(company = company).order_by('-dateTime').first().totalCourseAmount
    except:
        return None

def get_company_instance_through_user_company(user):
    try:
        return UserCompany.objects.get(user = user).company
    except: raise serializers.ValidationError('User have no company.')

def get_last_course_count_through_latest_course(company):
    try:
        return Course.objects.filter(company=company).order_by('-courseDateTime').first().courseCount
    except:
        return 0

def check_company_name(name):
    try:
        company = Company.objects.get(name = name)
    except:
        company = None
    if company !=  None:
        raise serializers.ValidationError('Company name taken.')
    
def get_course_count_through_bundle_price(bundle):
    try:
        return BundlePrice.objects.get(pk=bundle).courseBundle.courseAmount
    except:
        raise serializers.ValidationError('No active subscription.')