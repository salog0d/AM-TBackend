
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Test
from .serializers import TestSerializer

# Función auxiliar para verificar permisos de administrador
def is_admin_or_superuser(user):
    """
    Verifica si el usuario es superusuario o administrador.
    """
    return user.is_superuser or user.is_admin()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTest(request):
    """
    Vista para crear un nuevo test.
    
    Esta vista está restringida a superusuarios y solo acepta solicitudes POST con
    carga útil JSON. Procesa la solicitud para crear una nueva instancia de test en la
    base de datos.
    
    Parámetros:
        request (HttpRequest): El objeto de solicitud HTTP que contiene información
        del usuario y datos de la solicitud.
        
    Retorna:
        Response: 
            - En caso de éxito: Una respuesta JSON con un mensaje de éxito y estado HTTP 201.
            - En caso de fallo: Una respuesta JSON con un mensaje de error y un código
              de estado HTTP apropiado:
                - 403: Si el usuario no es superusuario.
                - 400: Si el método de solicitud no es POST o los datos JSON son inválidos.
    """
    if not request.user.is_superuser:
        return Response({"status": "error", "message": "No tiene permiso para crear test"}, 
                      status=status.HTTP_403_FORBIDDEN)

    serializer = TestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success", 
            "message": "Test creado correctamente"
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "status": "error", 
        "message": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def viewTests(request):
    """
    Vista para obtener todos los tests.
    
    Esta función recupera y devuelve una lista de todos los tests en la base de datos.
    Garantiza que solo superusuarios o usuarios con privilegios de administrador puedan
    acceder a la lista de tests.
    
    Parámetros:
        request (HttpRequest): El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
        
    Retorna:
        Response:
            - Si el usuario está autorizado: Una respuesta JSON que contiene una lista de todos
              los tests con un código de estado 200.
            - Si el usuario carece de los permisos necesarios: Una respuesta JSON con un mensaje
              de error y un código de estado 403.
    """
    if is_admin_or_superuser(request.user):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response({"tests": serializer.data}, status=status.HTTP_200_OK)

    return Response({
        "status": "error", 
        "message": "No tiene permiso para ver tests"
    }, status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTest(request, test_id):
    """
    Vista para eliminar un test.
    
    Esta función permite a un superusuario o un usuario administrador eliminar un test
    identificado por su `test_id`. Si el usuario no tiene los permisos requeridos,
    se devuelve una respuesta JSON con un mensaje de error y un código de estado 403.
    
    Parámetros:
        request (HttpRequest): El objeto de solicitud HTTP que contiene metadatos
            sobre la solicitud.
        test_id (int): El ID del test a eliminar.
            
    Retorna:
        Response: Una respuesta JSON que indica el éxito o fracaso de la operación
            de eliminación. En caso de éxito, se devuelve un código de estado 200
            con un mensaje de éxito. En caso de fallo debido a permisos insuficientes,
            se devuelve un código de estado 403 con un mensaje de error.
            
    Permisos:
        - El usuario debe ser superusuario o tener privilegios de administrador para eliminar un test.
    """
    if is_admin_or_superuser(request.user):
        test = get_object_or_404(Test, id=test_id)
        test.delete()
        return Response({
            "status": "success", 
            "message": "Test eliminado correctamente"
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error", 
            "message": "No tiene permiso para eliminar test"
        }, status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateTest(request, test_id):
    """
    Vista para actualizar un test existente.
    
    Esta función permite a usuarios autorizados actualizar los detalles de un test específico.
    Garantiza que solo superusuarios o usuarios con privilegios de administrador puedan realizar
    la actualización. La función espera una solicitud con una carga útil JSON que contenga
    los detalles actualizados del test.
    
    Parámetros:
        request (HttpRequest): El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
        test_id (int): El ID del test a actualizar.
            
    Retorna:
        Response: Una respuesta JSON que indica el éxito o fracaso de la operación de actualización.
            - En caso de éxito: Devuelve un objeto JSON con un mensaje de éxito y estado HTTP 200.
            - En caso de fallo: Devuelve un objeto JSON con un mensaje de error y estado HTTP apropiado:
                - 403 si el usuario carece de permisos.
                - 400 si los datos JSON son inválidos.
    """
    if not is_admin_or_superuser(request.user):
        return Response({
            "status": "error", 
            "message": "No tiene permiso para actualizar test"
        }, status=status.HTTP_403_FORBIDDEN)
    
    test = get_object_or_404(Test, id=test_id)
    serializer = TestSerializer(test, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success", 
            "message": "Test actualizado correctamente"
        }, status=status.HTTP_200_OK)
    
    return Response({
        "status": "error", 
        "message": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def viewTest(request, test_id):
    """
    Vista para ver un test específico.
    
    Esta función recupera y devuelve los detalles de un test identificado por su `test_id`.
    Garantiza que solo superusuarios o usuarios con privilegios de administrador puedan
    acceder a los detalles del test.
    
    Parámetros:
        request (HttpRequest): El objeto de solicitud HTTP que contiene metadatos sobre la solicitud.
        test_id (int): El identificador único del test a recuperar.
            
    Retorna:
        Response:
            - Si el usuario está autorizado y el test existe:
                Una respuesta JSON que contiene los detalles del test con un código de estado 200.
            - Si el test no existe:
                Una respuesta JSON con un mensaje de error y un código de estado 404.
            - Si el usuario carece de los permisos necesarios:
                Una respuesta JSON con un mensaje de error y un código de estado 403.
    """
    if is_admin_or_superuser(request.user):
        try:
            test = get_object_or_404(Test, id=test_id)
            serializer = TestSerializer(test)
            return Response({"test": serializer.data}, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            return Response({
                "status": "error", 
                "message": "Test no encontrado"
            }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "status": "error", 
        "message": "No tiene permiso para ver test"
    }, status=status.HTTP_403_FORBIDDEN)

