"""
Views for the Attendance APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Attendance
from attendance import serializers



# Create your views here.
class AttendanceViewSet(viewsets.ModelViewSet):
    """View for manage attendance APIs"""
    serializer_class = serializers.AttendanceDetailSerializer
    queryset = Attendance.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve attendances for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.AttendanceSerializer
        
        return self.serializer_class
    
    
    def perform_create(self, serializer):
        """Create a new attendance""" 
        serializer.save(user=self.request.user)


    def create(self, request, *args, **kwargs):
        """Create a new attendance with latitude and longitude validation"""
        latitude = float(request.data.get('latitude'))
        longitude = float(request.data.get('longitude'))

        # Define the preset range (for example purposes)
        min_latitude = 3.0
        max_latitude = 5.0
        min_longitude = 6.0
        max_longitude = 7.0

        # Perform validation
        if (min_latitude <= latitude <= max_latitude) and (min_longitude <= longitude <= max_longitude):
            # Latitude and longitude fall within the preset range
            return super().create(request, *args, **kwargs)
        else:
            # Latitude and longitude are outside the preset range
            return Response({'Error': 'Latitude and longitude values are outside the valid range'}, status=status.HTTP_400_BAD_REQUEST)
