from core.models import *
from rest_framework import serializers



class CleaningServiceUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningServiceUserProfile
        fields = ['profile_id', 'first_name', 'last_name', 'contact', 'profile_image', 'time_created']


class CleaningServiceSerializer(serializers.ModelSerializer):
    profile = CleaningServiceUserProfileSerializer()
    class Meta:
        model = CleaningServiceUser
        fields = ['user_id', 'email', 'user_type','organization_name', 'profile']
        # extra_kwargs = {'password': {'write_only': True}, 'is_active': {'read_only': True}, 'is_staff': {'read_only': True}, 'is_superuser': {'read_only': True},}
        
        
        
class VerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class PasswordTokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        


class ServiceSerializer(serializers.ModelSerializer):
    
    user = CleaningServiceSerializer(read_only=True)
    class Meta:
        model = Service
        fields = ['service_id', 'user', 'title', 'description', 'price', 'thumnail', 'created_at']
        extra_kwargs = {'service_id': {'read_only': True}}
        
class ScheduleServiceSerializer(serializers.ModelSerializer):
    """Schedule Service Serializer

    Args:
        serializers (dict): model serializer for schedule service
    """
    service = ServiceSerializer(many=False, read_only=True)
    customer = CleaningServiceSerializer(many=False, read_only=True)
    class Meta:
        model = ScheduleService
        fields = "service", "customer", 'date', "time", "status"


class ServiceFeedbackSerialiazer(serializers.ModelSerializer):
    """Service Feedback Serializer"""

    class Meta:
        model = ServiceFeedback
        fields = "__all__"
        
    
class NotificationSerializer(serializers.ModelSerializer):
    """Notification Serializer"""

    class Meta:
        model = Notification
        fields =   "__all__"