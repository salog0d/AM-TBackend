from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.custom_auth.models import CustomUser
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token



def is_admin():
    pass


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, custom_user_id):
    """from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
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
@permission_classes([IsAuthenticated])
def logoutUser(request):
    """
    Logs out the user by deleting their token.
    """
    try:
        # Delete the user's token
        request.user.auth_token.delete()
        return Response({
            'status': 'success',
            'message': 'Usuario desconectado correctamente'
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Error al cerrar sesión: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

