from rest_framework import serializers
from apps.custom_auth.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo CustomUser.
    Gestiona la serialización y deserialización de instancias de CustomUser.
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'profile_picture', 
                  'role', 'discipline', 'date_of_birth', 'phone_number']
    
    def create(self, validated_data):
        """
        Crea y devuelve un nuevo usuario con contraseña cifrada.
        """
        password = validated_data.pop('password', None)
        # Use create_user instead of create to properly handle password hashing
        user = CustomUser.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email', ''),
            password=password,
            **validated_data
        )
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
