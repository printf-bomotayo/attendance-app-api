"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import requests
from core import models

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """"Test creating a user with an email is successful"""

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password=password
        )

        self.assertEqual(user.email, email) 
        self.assertEqual(user.check_password(password), True) 
        # self.assertTrue(user.check_password(password))  ## Alternative syntax to line of code directly above 

    def test_new_user_email_normalized(self):
        """TEst email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)


    def new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        # Assertions
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)



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



    def test_create_attendance_with_coordinates(self):
        """Test creating an attendance with coordinates matching preset values"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        # Get the current date and time
        current_datetime = timezone.now()

        # Set the status based on the hour
        if current_datetime.hour < 8:
            status = 'Early'
        else:
            status = 'Late'
        
        # Get the current coordinates
        # current_coordinates = self.get_current_coordinates()
        current_coordinates = [6.535098, 3.369131]

        if current_coordinates:
            # Set the preset coordinates for comparison
            preset_latitude = 6.000100
            preset_longitude = 3.000100
            # Check if the current coordinates match the preset values
            if (
                (current_coordinates[0] >= preset_latitude and current_coordinates[0] <= 7.0050)
                and 
                (current_coordinates[1] >= preset_longitude and current_coordinates[1] <= 4.00050)
            ):


                attendance = models.Attendance.objects.create(
                    user=user,
                    date=current_datetime.date(),
                    time=current_datetime.time(),
                    status=status,
                    latitude=current_coordinates[0],
                    longitude=current_coordinates[1]
                )

                # Assertions
                self.assertEqual(attendance.user, user)
                self.assertEqual(attendance.date, current_datetime.date())
                self.assertEqual(attendance.time, current_datetime.time())
                self.assertEqual(attendance.status, status)
                self.assertEqual(attendance.latitude, current_coordinates[0])
                self.assertEqual(attendance.longitude, current_coordinates[1])

            else:
                # Coordinates do not match
                print('Coordinates do not match preset values')

        else:
            # Unable to get current coordinates
            print('Unable to get current coordinates')