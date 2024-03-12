"""
Views for the User Api
"""

from rest_framework import generics
from user.serializers import UserSerializer

# from django.shortcuts import render


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer