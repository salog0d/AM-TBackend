from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from apps.custom_auth.models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, UserRegisterSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def is_admin(user):
    """
    Verifica si un usuario tiene rol de administrador.
    """
    return user.role == 'admin' or user.is_superuser


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Vista para el registro de usuarios.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Usuario creado exitosamente',
                'user': serializer.data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, custom_user_id):
    """
    Elimina un usuario del sistema basado en el ID proporcionado.
    
    Esta vista está restringida a superusuarios o usuarios con privilegios de administrador.
    """
    if not is_admin(request.user):
        return Response({
            'status': 'error',
            'message': 'No tienes permiso para eliminar un usuario'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = CustomUser.objects.get(id=custom_user_id)
        user.delete()
        return Response({
            'status': 'success',
            'message': 'Usuario eliminado correctamente'
        })
    except CustomUser.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Usuario no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'PATCH', 'POST'])
@permission_classes([IsAuthenticated])
def updateUser(request, custom_user_id):
    """
    Actualiza la información de un usuario.
    
    Esta vista está restringida a superusuarios y usuarios administradores.
    """
    if not is_admin(request.user):
        return Response({
            'status': 'error',
            'message': 'No tienes permiso para actualizar un usuario'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = CustomUser.objects.get(id=custom_user_id)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Usuario actualizado correctamente'
            })
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Usuario no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request, custom_user_id):
    """
    Obtiene los detalles de un usuario por ID.
    
    Esta vista está restringida a superusuarios y usuarios administradores.
    """
    if not is_admin(request.user):
        return Response({
            'status': 'error',
            'message': 'No tienes permiso para ver esta página'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = CustomUser.objects.get(id=custom_user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Usuario no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listUsers(request):
    """
    Maneja el listado de usuarios en formato JSON.
    
    Esta vista está restringida a usuarios con privilegios administrativos.
    """
    if request.user.is_staff or request.user.is_superuser:
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response({"Users": serializer.data})
    
    return Response({
        "status": "error",
        "message": "No tienes permiso para ver esta página"
    }, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def logoutUser(request):
    """
    Invalida el token de refresco del usuario actual (logout).
    """
    try:
        refresh_token = request.data.get("refresh")  # Usar paréntesis en lugar de corchetes
        
        if not refresh_token:
            return Response({
                'status': 'error',
                'message': 'Token de refresco no proporcionado'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        token = RefreshToken(refresh_token)
        token.blacklist()     
        return Response({
            'status': 'success',
            'message': 'Sesión cerrada correctamente'
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    """
    Obtiene el perfil del usuario autenticado actual.
    """
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)