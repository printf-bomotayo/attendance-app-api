"""
Serializers for attendance API
"""

from rest_framework import serializers
from core.models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for attendance"""

    status = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'date', 'time', 'status', 'latitude', 'longitude']
        read_only_fields = ['id', 'status'] #fields  ## come back to change so that a user can only have read-only access after an attendance object has been created

    def get_status(self, obj):
        """Dynamically determine the status based on time"""
        if obj.time.hour < 8:
            return 'Early'
        else:
            return 'Late'

class AttendanceDetailSerializer(AttendanceSerializer):
    """Serializer for attendance detail view."""
    
    class Meta(AttendanceSerializer.Meta):
        fields = AttendanceSerializer.Meta.fields
