# views.py (Dashboard views)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.custom_auth.models import CustomUser
from .serializers import CustomUserSerializer, TestResultSerializer

"""
Este módulo contiene las diferentes vistas para el dashboard
Estas vistas son responsables de mostrar los datos del dashboard y gestionar datos de usuarios.

Las vistas incluyen:
- admin_dashboard: Muestra el dashboard de administrador y recupera todos los usuarios del sistema.
- coach_dashboard: Muestra el dashboard de entrenador y recupera todos los atletas asociados a un entrenador específico.
- athlete_dashboard: Muestra el dashboard de atleta y recupera los detalles de un atleta específico.
"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def adminDashboard(request):
    """
    Vista del dashboard de administrador.

    Esta vista recupera todos los usuarios en el sistema y devuelve sus detalles.
    Asegura que el usuario solicitante esté autenticado y tenga el rol de administrador.
    """
    # Verificar si el usuario está autenticado y tiene rol de administrador
    if request.user.is_authenticated and request.user.is_admin():
        try:
            # Recuperar todos los usuarios del sistema con información del coach
            users = CustomUser.objects.select_related('coach').all()
            serializer = CustomUserSerializer(users, many=True)
            
            # Devolver respuesta exitosa con la lista de usuarios
            return Response({
                'status': 'success',
                'users': serializer.data
            })
        except Exception as e:
            # Manejar caso donde ocurre un error al recuperar usuarios
            return Response({
                'status': 'error',
                'message': f'Error al recuperar usuarios: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # Devolver error de permiso si el usuario no está autorizado para acceder a esta vista
        return Response({
            'status': 'error',
            'message': 'No tiene permiso para ver esta página'
        }, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def coachDashboard(request, custom_user_id):
    """
    Vista del dashboard de entrenador.

    Esta vista recupera todos los atletas asociados a un entrenador específico.
    Asegura que el usuario solicitante esté autenticado y tenga el rol de entrenador.
    """
    try:
        # Verificar que el usuario autenticado sea un entrenador o un administrador
        if request.user.role != 'coach' and request.user.role != 'admin':
            return Response({
                'status': 'error',
                'message': 'Solo los entrenadores pueden acceder a esta vista'
            }, status=status.HTTP_403_FORBIDDEN)
            
        # Recuperar el objeto de usuario entrenador basado en el ID proporcionado y rol
        coach = get_object_or_404(CustomUser, id=custom_user_id, role='coach')
      
        # Recuperar atletas con información del coach usando select_related para optimizar
        athletes = CustomUser.objects.select_related('coach').filter(coach=coach)
        
        print(f"Coach ID: {coach.id}, Coach Username: {coach.username}")
        print(f"Número de atletas encontrados: {athletes.count()}")
        
        # Serializar y devolver los atletas
        serializer = CustomUserSerializer(athletes, many=True)
        print("Datos serializados:", serializer.data)
        
        # Devolver respuesta exitosa con la lista de atletas
        return Response({
            'status': 'success',
            'athletes': serializer.data
        })
    except Exception as e:
        # Capturar y registrar cualquier excepción no manejada
        print(f"Error en coachDashboard: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def athleteDashboard(request, custom_user_id):
    """
    Vista del dashboard de atleta.
    
    Esta vista recupera los detalles de un atleta específico.
    Asegura que el usuario solicitante esté autenticado y tenga el rol de atleta.
    """
    if request.user.is_authenticated:
        try:
            # Recuperar el objeto de usuario atleta basado en el ID proporcionado y rol
            # Usar select_related para incluir información del coach en una sola consulta
            athlete = get_object_or_404(
                CustomUser.objects.select_related('coach'), 
                id=custom_user_id, 
                role='athlete'
            )
            serializer = CustomUserSerializer(athlete)
            
            # Devolver respuesta exitosa con los detalles del atleta
            return Response({
                'status': 'success',
                'athlete': serializer.data
            })
        except CustomUser.DoesNotExist:
            # Manejar caso donde el atleta no existe
            return Response({
                'status': 'error',
                'message': 'Atleta no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        # Devolver error de permiso si el usuario no está autorizado para acceder a esta vista
        return Response({
            'status': 'error',
            'message': 'No tiene permiso para ver esta página'
        }, status=status.HTTP_403_FORBIDDEN)


"""
Esta sección contiene las diferentes vistas para los detalles del dashboard
Estas vistas son responsables de mostrar los detalles del dashboard y gestionar datos de usuarios.
"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def athleteDetails(request, custom_user_id):
    """
    Vista de detalles de atleta.
    
    Esta vista recupera los detalles de un atleta específico basado en su ID.
    Asegura que el usuario solicitante esté autenticado y tenga el rol apropiado.
    """
    if request.user.is_authenticated and request.user.is_coach():
        try:
            # Recuperar el objeto de usuario atleta basado en el ID proporcionado y rol
            athlete = get_object_or_404(
                CustomUser.objects.select_related('coach'), 
                id=custom_user_id, 
                role='athlete'
            )
            serializer = CustomUserSerializer(athlete)
            
            # Devolver respuesta exitosa con los detalles del atleta
            return Response({
                'status': 'success',
                'athlete': serializer.data
            })
        except CustomUser.DoesNotExist:
            # Manejar caso donde el atleta no existe
            return Response({
                'status': 'error',
                'message': 'Atleta no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        # Devolver error de permiso si el usuario no está autorizado para acceder a esta vista
        return Response({
            'status': 'error',
            'message': 'No tiene permiso para ver esta página'
        }, status=status.HTTP_403_FORBIDDEN)


"""
Esta sección contiene las diferentes vistas para las pruebas que aparecen para cada atleta
Estas vistas son responsables de mostrar las pruebas y gestionar datos de usuarios.
"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def testResults(request, custom_user_id):
    """
    Vista de resultados de pruebas para un atleta específico.

    Esta vista recupera los resultados de pruebas asociados con un atleta específico.
    Asegura que el usuario solicitante esté autenticado y tenga el rol apropiado
    (administrador, entrenador, o el atleta mismo) para acceder a los datos.
    """
    # Recuperar el objeto atleta basado en el ID proporcionado y rol, o devolver un 404 si no se encuentra
    athlete = get_object_or_404(CustomUser, id=custom_user_id, role='athlete')

    # Verificar el rol del usuario solicitante y validar permisos
    if request.user.is_admin():
        # Los administradores pueden acceder a los resultados de pruebas para todos los atletas
        pass
    elif request.user.is_coach():
        # Los entrenadores solo pueden acceder a los resultados de pruebas para atletas con los que están asociados
        if athlete.coach != request.user:
            return Response({
                'status': 'error',
                'message': 'No tiene permiso para ver este atleta'
            }, status=status.HTTP_403_FORBIDDEN)
    elif request.user.is_athlete() and request.user.id != athlete.id:
        # Los atletas solo pueden ver sus propios resultados
        return Response({
            'status': 'error',
            'message': 'No tiene permiso para ver resultados de otros atletas'
        }, status=status.HTTP_403_FORBIDDEN)
    else:
        # Devolver error de permiso si el usuario no tiene un rol válido
        return Response({
            'status': 'error',
            'message': 'No tiene permiso para ver esta página'
        }, status=status.HTTP_403_FORBIDDEN)

    # Recuperar y serializar los resultados de pruebas para el atleta
    # Usar select_related para optimizar las consultas
    test_results = athlete.test_results.select_related('test', 'session').all()
    serializer = TestResultSerializer(test_results, many=True)

    # Devolver respuesta exitosa con los resultados de pruebas
    return Response({
        'status': 'success',
        'test_results': serializer.data
    })