from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import json

from django.contrib.auth import authenticate, login, logout


from apps.custom_auth.models import CustomUser
from .serializers import CustomUserSerializer, UserLoginSerializer

def is_admin(user):
    """
    Función auxiliar para comprobar si un usuario es administrador o superusuario.
    """
    return user.is_superuser or user.is_admin()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createUser(request):
    """
    Crea un nuevo usuario.
    
    Esta vista está restringida a superusuarios y usuarios administradores.
    """
    if not is_admin(request.user):
        return Response({
            'status': 'error',
            'message': 'No tienes permiso para crear un usuario'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'message': 'Usuario creado correctamente'
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
@permission_classes([AllowAny])
def loginUser(request):
    """
    Autentica y conecta a un usuario basado en las credenciales proporcionadas.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'status': 'success',
                'message': 'Usuario conectado correctamente',
                'user_id': user.id
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Nombre de usuario o contraseña inválidos'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'status': 'error',
        'message': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    """
    Cierra la sesión del usuario autenticado actualmente.
    """
    logout(request)
    return Response({
        'status': 'success',
        'message': 'Usuario desconectado correctamente'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    """
    Cambia la contraseña del usuario autenticado actualmente.
    """
    try:
        data = request.data
        current_password = data['current_password']
        new_password = data['new_password']
        
        # Verificar contraseña actual
        user = request.user
        if not user.check_password(current_password):
            return Response({
                'status': 'error',
                'message': 'La contraseña actual es incorrecta'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Establecer y cifrar la nueva contraseña
        user.set_password(new_password)
        user.save()
        
        # Volver a autenticar al usuario con la nueva contraseña
        login(request, user)
        
        return Response({
            'status': 'success',
            'message': 'Contraseña cambiada correctamente'
        })
    
    except KeyError as e:
        return Response({
            'status': 'error',
            'message': f'Campo faltante: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
