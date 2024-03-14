"""
URL mappings for the attendance app
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from attendance import views


router = DefaultRouter()

router.register('attendances', views.AttendanceViewSet)

app_name = 'attendance'

urlpatterns = [
    path('', include(router.urls)),
]