from rest_framework import routers
from .views import *
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.SimpleRouter()
router.register(r'users', UserViewSets, basename='users')
router.register(r'companies', CompanyViewSets, basename='companies')
router.register(r'user-companies', UserCompanyViewSets, basename='user-companies')
router.register(r'courses', CourseViewSets, basename='courses')
router.register(r'user-courses', UserCourseViewSets, basename='user-courses')
router.register(r'course-bundles', CourseBundleViewSets, basename='course-bundles')
router.register(r'bundle-prices', BundlePriceViewSets, basename='bundle-prices')
router.register(r'company-course-bundles', CompanyCourseBundleViewSets, basename='company-course-bundles')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
urlpatterns += router.urls