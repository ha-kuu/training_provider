from drf_spectacular.utils import OpenApiResponse, OpenApiRequest, OpenApiParameter, OpenApiExample, extend_schema
from .drf_spec_msg_serializer import *
from .serializers import *

description = ''

parameters = ''

response_dsoa = {
    200:OpenApiResponse(description='[Success]')
}

get_company_st = 'Get company info. [Company\'s user]'
post_company_st = 'Create company and link creator to the company. [Company\'s user]'
post_company_course_bundle_st = 'Let company choose subscription to use. [Company\'s user]'
get_course_company_st = 'Get courses made by company with their participants. [Company\'s user]'
get_course_user_st = 'Get currently available company. [Basic user]'
post_course_st = 'Create course. [Company\'s user]'
get_specific_course_st = 'Get course info. [Both user type]'
post_user_course_st = 'Basic user join a course. [Basic user]'
get_company_user_st = 'Get list of user in the same company. [Company\'s user]'
post_user_st = 'Create new user. [Both user]'
get_specific_user_st = 'Only get own full info with encrypted password. [Both user type]'

not_target_user_400_st = '{Not Authorized.}'
no_auth_response_401_st = {"detail": "Authentication credentials were not provided."}


es_desc = ''
es_param = ''
es_response = {}

dsoa = {
    'description' : '',
    'parameters' : None,
    'responses' : {
        200:UserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_list_company = {
    'description' : get_company_st,
    'parameters' : None,
    'responses' : {
        200:GetUserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_post_company = {
    'description' : post_company_st,
    'parameters' : None,
    'responses' : {
        200:PostUserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_post_company_course_bundle = {
    'description' : post_company_course_bundle_st,
    'parameters' : None,
    'responses' : {
        200:UserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_list_course = {
    'description' : get_course_company_st,
    'parameters' : None,
    'responses' : {
        200:UserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_post_course = {
    'description' : post_course_st,
    'parameters' : None,
    'responses' : {
        200:UserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_retrieve_course = {
    'description' : get_specific_course_st,
    'parameters' : None,
    'responses' : {
        200:GetUserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_list_user = {
    'description' : get_company_user_st,
    'parameters' : None,
    'responses' : {
        200:GetUserSerializer(many=True),
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_post_user = {
    'description' : post_user_st,
    'parameters' : None,
    'responses' : {
        200:UserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}

dsoa_retrieve_user = {
    'description' : get_specific_user_st,
    'parameters' : None,
    'responses' : {
        200:UserSerializer,
        400:not_target_user_400_st,
        401:no_auth_response_401_st
    }
}
class DataNotValidSerializer(serializers.Serializer):
    'Data not valid.'