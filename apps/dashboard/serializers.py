from rest_framework import serializers
from apps.custom_auth.models import CustomUser
from apps.lab.models import TestResult  # Ajusta la importación según tu modelo real

from rest_framework import serializers
from apps.custom_auth.models import CustomUser
from apps.lab.models import TestResult

class CoachSummarySerializer(serializers.ModelSerializer):
    """Serializer simplificado para información básica del coach"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'email', 'discipline', 'phone_number']

class CustomUserSerializer(serializers.ModelSerializer):
    coach_details = CoachSummarySerializer(source='coach', read_only=True)
    coach_username = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'name', 'email', 'role', 'discipline',
            'date_of_birth', 'phone_number', 'coach', 'coach_username', 'coach_details'
        ]

    def get_coach_username(self, obj):
        return obj.coach.username if obj.coach else None

class TestResultSerializer(serializers.ModelSerializer):
    """Serializador para el modelo TestResult."""
    test_name = serializers.CharField(source='test.name', read_only=True)
    test_unit = serializers.CharField(source='test.unit', read_only=True)
    test_category = serializers.CharField(source='test.category', read_only=True)
    test_higher_is_better = serializers.BooleanField(source='test.higher_is_better', read_only=True)
    
    class Meta:
        model = TestResult
        fields = ['id', 'athlete', 'test', 'session', 'numeric_value', 
                 'notes', 'date_recorded', 'test_name', 'test_unit', 
                 'test_category', 'test_higher_is_better']