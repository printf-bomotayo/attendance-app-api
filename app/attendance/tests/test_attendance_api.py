"""
Tests for Attendance APIs.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Attendance
from attendance.serializers import (
    AttendanceSerializer,
    AttendanceDetailSerializer
    )
from datetime import datetime

from django.utils import timezone
import requests
from core import models


ATTENDANCES_URL= reverse('attendance:attendance-list')

def detail_url(attendance_id):
    """Create and return an attendance detail url."""
    return reverse('attendance:attendance-detail', args=[attendance_id])



# Given date and time strings
date_str = '2022-03-15'
time_str = '07:30:00'
# Convert to date and time objects
date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
time_object = datetime.strptime(time_str, '%H:%M:%S').time()

def create_attendance(user, **params):
    """Create and return a sample attendance object."""
    defaults = {
            'date': date_object,
            'time': time_object,
            'status': 'Early',
            'latitude': Decimal('6.74477'),
            'longitude': Decimal('7.38479'),
    }

    defaults.update(params)
    attendance = Attendance.objects.create(user=user, **defaults)
    return attendance



def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicAttendanceAPITests(TestCase):
    """Test unauthorized API requets"""
    def setUp(self):
        self.client = APIClient()

def test_auth_required(self):
    """Test auth is required to call API"""
    res = self.client.get(ATTENDANCES_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAttendanceApiTests(TestCase):
    """Test authenticated API requests."""

    def create_attendance_payload(self):
        """Create payload for attendance post request."""
        # Get the current date and time
        current_datetime = datetime.now()

        # Set the status based on the hour
        if current_datetime.hour < 8:
            status = 'Early'
        else:
            status = 'Late'

        # Construct the payload
        payload = {
            'date': current_datetime.strftime('%Y-%m-%d'),
            'time': current_datetime.strftime('%H:%M:%S'),  
            'status': status,
            'latitude': 4.0,  
            'longitude': 6.5,
        }

        return payload

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        # self.user = get_user_model().objects.create_user(
        #     'user@example.com',
        #     'testpass123',
        # )
        self.client.force_authenticate(self.user)

    def test_retrieve_attendances(self):
        """Test retrieving a list of attendances"""

        create_attendance(user=self.user)
        create_attendance(user=self.user)

        res = self.client.get(ATTENDANCES_URL)

        attendances = Attendance.objects.all().order_by('-id')

        serializer = AttendanceSerializer(attendances, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)



    def test_attendance_list_limited_to_user(self):
        """Test list of attendances is limited to authenticated user."""
        # other_user = get_user_model().objects.create_user(
        #     'other@example.com',
        #     'password123'
        # )
        other_user = create_user(email="other@example.com", password="password123")
        create_attendance(user=other_user)
        create_attendance(user=self.user)

        res = self.client.get(ATTENDANCES_URL)
        attendances = Attendance.objects.filter(user=self.user)
        serializer = AttendanceSerializer(attendances, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
        
    
    def test_get_attendance_detail(self):
        """Test get attendance detail"""
        attendance = create_attendance(user=self.user)

        url = detail_url(attendance.id)
        res = self.client.get(url)
        serializer = AttendanceDetailSerializer(attendance)
        self.assertEqual(res.data, serializer.data)

    
    # def test_create_attendance(self):
    #     """Test creating attendance."""
    #     payload = {
    #         'date': date_object,
    #         'time': time_object,
    #         'status': 'Early',
    #         'latitude': Decimal('6.74477'),
    #         'longitude': Decimal('7.38479'),
    #     }
    #     res = self.client.post(ATTENDANCES_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     attendance = Attendance.objects.get(id=res.data['id'])
    #     for k, v in payload.items():
    #         self.assertEqual(getattr(attendance, k), v)

    #     self.assertEqual(attendance.user, self.user)


    # def get_current_coordinates(self):
    #     """Get current coordinates using google maps API."""
    #     api_key = 'API_KEY'
    #     url = 'https://maps.googleapis.com/maps/api/geocode/json'

    #     try:
    #         # Make a request to get the user's current location based on IP address
    #         response = requests.get(f'{url}?key={api_key}')
    #         data = response.json()

    #         # Check if the response is successful
    #         if response.status_code == 200 and data.get('status') == 'OK':
    #             # Extract latitude and longitude from the response
    #             location = data['results'][0]['geometry']['location']
    #             latitude = location['lat']
    #             longitude = location['lng']

    #             return latitude, longitude

    #         else:
    #             # Handle unsuccessful response
    #             print(f'Error: {data.get("status")}')
    #             return None

    #     except requests.exceptions.RequestException as e:
    #         # Handle request exception
    #         print(f'Request Exception: {e}')
    #         return None


    def test_create_attendance(self):
        """Test creating an attendance."""

        # Create payload for attendance post request
        payload = self.create_attendance_payload()

        # Make post request
        res = self.client.post(ATTENDANCES_URL, payload)

        # Check if the post request was successful
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Check if the attendance object was created
        attendance = models.Attendance.objects.get(id=res.data['id'])

        # Check user association
        self.assertEqual(attendance.user, self.user)

        # Check date
        self.assertEqual(attendance.date.strftime('%Y-%m-%d'), payload['date'])

        # Check time
        self.assertEqual(attendance.time.strftime('%H:%M:%S'), payload['time'])

        print("Attendance: ", attendance.status)

        print("Payload['status']: ", payload['status'])
        # Check status
        self.assertEqual(attendance.status, payload['status'])

        # Check latitude
        self.assertEqual(attendance.latitude, payload['latitude'])

        # Check longitude
        self.assertEqual(attendance.longitude, payload['longitude'])