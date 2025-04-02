from django.contrib.auth.decorators import login_required
from django.shortcuts import JsonResponse

from custom_auth.models import CustomUser

#Create User
@login_required(login_url='/login/')
def create_User(request):
    return JsonResponse({
        'status': 'success',
        'message': 'User created successfully'
    })

#Delete User
def delete_User(request, custom_user_id):
    return JsonResponse({
        'status': 'success',
        'message': 'User deleted successfully'
    })

#Update User
def update_User(request, custom_user_id):
    return JsonResponse({
        'status': 'success',
        'message': 'User updated successfully'
    })

#List Users
def list_Users(request):
    if request.user.is_admin() or request.user.is_superuser:
        users = list(CustomUser.objects.values("id"))
        return JsonResponse({"Users": users})
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to view this page'
        })


#Login User
def login_User(request):
    return JsonResponse({
        'status': 'success',
        'message': 'User logged in successfully'
    })


#Logout User
def logout_User(request):
    return JsonResponse({
        'status': 'success',
        'message': 'User logged out successfully'
    })


#Change Password
def change_Password(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Password changed successfully'
    })