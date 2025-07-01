from rest_framework import serializers
from apps.custom_auth.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo CustomUser.
    Gestiona la serialización y deserialización de instancias de CustomUser.
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'profile_picture', 
                  'role', 'discipline', 'date_of_birth', 'phone_number',"coach"]
    
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para obtener tokens JWT con información adicional.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadir datos personalizados al token
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['discipline'] = user.discipline
        token['active'] = user.is_active

        return token
        
    def validate(self, attrs):
        # This method gets called during token creation
        data = super().validate(attrs)
        
        # Add these fields to the response directly
        user = self.user
        data['user_id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['role'] = user.role
        data['discipline'] = user.discipline
        data['is_active'] = user.is_active
        
        return data


# Reemplaza el UserRegisterSerializer en apps/custom_auth/serializers.py

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro de usuarios con generación de tokens JWT.
    """
    password = serializers.CharField(write_only=True)
    coach = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='coach'),
        required=False,
        allow_null=True
    )
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'profile_picture',
                  'role', 'discipline', 'date_of_birth', 'phone_number', 'coach', 'tokens']

    def validate(self, data):
        """Validaciones personalizadas."""
        role = data.get('role')
        coach = data.get('coach')
        
        # Solo los atletas pueden tener coach
        if role != 'athlete' and coach is not None:
            raise serializers.ValidationError("Solo los atletas pueden tener un coach asignado.")
        
        # Si es atleta y se asigna coach, verificar que el coach tenga rol 'coach'
        if role == 'athlete' and coach is not None:
            if coach.role != 'coach':
                raise serializers.ValidationError("El usuario asignado como coach debe tener el rol de coach.")
        
        return data

    def get_tokens(self, user):
        """
        Genera tokens JWT para el usuario.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        """
        Crea un nuevo usuario con contraseña cifrada y genera tokens JWT.
        """
        
        password = validated_data.pop('password', None)
        coach = validated_data.get('coach', None)
        
        
        user = CustomUser.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email', ''),
            password=password,
            **validated_data
        )

        return user