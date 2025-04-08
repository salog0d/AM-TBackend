from rest_framework import serializers
from apps.custom_auth.models import CustomUser
from apps.lab.models import TestResult  # Ajusta la importación según tu modelo real

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo CustomUser.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'email', 'role', 'discipline', 
                 'date_of_birth', 'phone_number']
        

class TestResultSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo TestResult.
    """
    class Meta:
        model = TestResult
        fields = ['id', 'athlete', 'test', 'session', 'numeric_value', 
                 'notes', 'date_recorded']



