# serializers.py
from rest_framework import serializers
from .models import Test

class TestSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Test.
    """
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'unit', 'category', 'higher_is_better']
