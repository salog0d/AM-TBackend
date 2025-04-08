from rest_framework import serializers
from apps.custom_auth.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo CustomUser.
    Gestiona la serialización y deserialización de instancias de CustomUser.
    """
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'profile_picture', 
                  'role', 'discipline', 'date_of_birth', 'phone_number']
    
    def create(self, validated_data):
        """
        Crea y devuelve un nuevo usuario con contraseña cifrada.
        """
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Actualiza y devuelve una instancia de usuario existente.
        """
        password = validated_data.pop('password', None)
        
        # Actualizar todos los campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Manejar la contraseña por separado
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer para validar las credenciales de inicio de sesión.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
