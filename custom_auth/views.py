import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from custom_auth.models import CustomUser

#Create User
@csrf_exempt
@login_required(login_url='custom_auth/login/')
def createUser(request):
    """
View to handle the creation of a new user.

This view is restricted to superusers and admin users. It processes POST requests
to create a new user in the system. The user data is expected to be provided in JSON
format in the request body.

Args:
    request (HttpRequest): The HTTP request object containing metadata about the request.

Returns:
    JsonResponse: A JSON response indicating the success or failure of the user creation process.

Raises:
    KeyError: If any required field is missing from the request data.

Notes:
    - The `@login_required` decorator ensures that only authenticated users can access this view.
    - The `request.user.is_superuser` and `request.user.is_admin()` checks restrict access to
      superusers and admin users.
    - The password provided in the request is hashed before saving the user to the database.
    - The following fields are expected in the request body:
        - username (str): The username of the new user.
        - email (str): The email address of the new user.
        - password (str): The password for the new user.
        - profile_picture (optional, str): The URL or path to the user's profile picture.
        - role (optional, str): The role assigned to the user.
        - discipline (optional, str): The discipline associated with the user.
        - date_of_birth (optional, str): The date of birth of the user.
        - phone_number (optional, str): The phone number of the user.
    """
    if not request.user.is_superuser and not request.user.is_admin():
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to create a user'
        })
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })
    # Assuming you have a form to create a user
    try:
        data = json.loads(request.body)
        user = CustomUser.objects.create(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            profile_picture=data.get('profile_picture'),
            role=data.get('role'),
            discipline=data.get('discipline'),
            date_of_birth=data.get('date_of_birth'),
            phone_number=data.get('phone_number')
        )
        user.set_password(data['password'])  # Hash the password
        user.save()
    except KeyError as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Missing field: {str(e)}'
        })
    return JsonResponse({
        'status': 'success',
        'message': 'User created successfully'
    })

#Delete User
@csrf_exempt
@login_required(login_url='custom_auth/login/')
def deleteUser(request, custom_user_id):
    """
Deletes a user from the system based on the provided user ID.

This view is restricted to superusers or users with admin privileges. 
If the user with the specified ID exists, they will be deleted from the database. 
If the user does not exist, an error response will be returned.

Args:
    request (HttpRequest): The HTTP request object containing metadata about the request.
    custom_user_id (int): The ID of the user to be deleted.

Returns:
    JsonResponse: A JSON response indicating the success or failure of the operation.
        - On success: {'status': 'success', 'message': 'User deleted successfully'}
        - On failure: {'status': 'error', 'message': 'User not found'}

Permissions:
    The requesting user must be a superuser or have admin privileges.

Raises:
    CustomUser.DoesNotExist: If the user with the specified ID does not exist.
    """
    if request.user.is_superuser or request.user.is_admin():
        try:
            user = CustomUser.objects.get(id=custom_user_id)
            user.delete()
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            })
    return JsonResponse({
        'status': 'error',
        'message': 'You dont have permissions'
    })

#Update User
@csrf_exempt
@login_required(login_url='custom_auth/login/')
def updateUser(request, custom_user_id):
    """
update_User(request, custom_user_id)

View function to update a user's information. This function is restricted to superusers 
and users with admin privileges. It handles updates to various user fields, including 
username, email, password, profile picture, role, discipline, date of birth, and phone number.

Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.
    custom_user_id (int): The ID of the user to be updated.

Returns:
    JsonResponse: A JSON response indicating the success or failure of the operation.

    - On success:
        {
        }
    - On failure:
        {
            'message': 'Error message describing the issue'
        }

Raises:
    KeyError: If a required field is missing from the request data.

Notes:
    - The request method must be POST; otherwise, an error response is returned.
    - Only superusers and users with admin privileges are authorized to perform this action.
    - If the 'password' field is provided in the request data, it is hashed before saving.
    """
    if not request.user.is_superuser and not request.user.is_admin():
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to update a user'
        })
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })
    try:
        data = json.loads(request.body)
        user = CustomUser.objects.get(id=custom_user_id)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.profile_picture = data.get('profile_picture', user.profile_picture)
        user.role = data.get('role', user.role)
        user.discipline = data.get('discipline', user.discipline)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.phone_number = data.get('phone_number', user.phone_number)
        if 'password' in data:
            user.set_password(data['password'])  # Hash the password
        user.save()
    except KeyError as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Missing field: {str(e)}'
        })
    return JsonResponse({
        'status': 'success',
        'message': 'User updated successfully'
    })

@csrf_exempt
@login_required(login_url='custom_auth/login/')
def getUser(request, custom_user_id):
    """
Retrieve user details by ID.

This view function retrieves the details of a specific user based on their ID.
Access to this endpoint is restricted to superusers and admin users. If the 
requesting user does not have the necessary permissions, an error response 
is returned.

Args:
    request (HttpRequest): The HTTP request object.
    custom_user_id (int): The ID of the user to retrieve.

Returns:
    JsonResponse: A JSON response containing the user's details if found, or 
    an error message if the user does not exist or the requester lacks 
    permissions.

Raises:
    CustomUser.DoesNotExist: If no user with the specified ID exists.

Permissions:
    - Superusers and admin users can access this endpoint.
    - Non-superusers and non-admin users will receive a permission error.

Response Structure:
    Success:
        {
            'id': int,
            'username': str,
            'email': str,
            'profile_picture': str or None,
            'role': str,
            'discipline': str,
            'date_of_birth': str,
            'phone_number': str
    Error:
        {
            'message': str
    """
    if not request.user.is_superuser and not request.user.is_admin():
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to view this page'
        })
    try:
        user = CustomUser.objects.get(id=custom_user_id)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'role': user.role,
            'discipline': user.discipline,
            'date_of_birth': user.date_of_birth,
            'phone_number': user.phone_number
        }
        return JsonResponse(user_data)
    except CustomUser.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'User not found'
        })

@csrf_exempt
@login_required(login_url='custom_auth/login/')
def listUsers(request):
    """
Handles the listing of users in JSON format.
This view is restricted to users with administrative privileges 
(staff or superuser). It retrieves and returns a list of users 
with specific fields such as ID, profile picture, role, name, 
discipline, date of birth, phone number, and email.
Access:
    - Requires the user to be authenticated.
    - Redirects unauthenticated users to the login page.
    - Returns a 403 error if the user lacks the required permissions.
Returns:
    JsonResponse: A JSON object containing the list of users if the 
    user has the necessary permissions.
    JsonResponse: A JSON object with an error message and a 403 
    status code if the user lacks permissions.
    """
    if request.user.is_staff or request.user.is_superuser:
        users = list(CustomUser.objects.values(
            "id", "profile_picture", "role", "name", 
            "discipline", "date_of_birth", "phone_number", "email"
        ))
        return JsonResponse({"Users": users})
    
    return JsonResponse({
        "status": "error",
        "message": "You do not have permission to view this page"
    }, status=403)

#Login User
@csrf_exempt
def loginUser(request):
    """
    Authenticates and logs in a user based on the provided credentials.
    
    This view processes POST requests containing user credentials (username and password)
    and attempts to authenticate the user. If authentication is successful, the user
    is logged in and a success response is returned. Otherwise, an error response is
    returned.
    
    Args:
        request (HttpRequest): The HTTP request object containing user credentials.
        
    Returns:
        JsonResponse: A JSON response indicating the success or failure of the login attempt.
        
    Notes:
        - The request method must be POST.
        - The request body must contain 'username' and 'password' fields.
        - If authentication fails, an error message is returned.
    """
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })
        
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': 'User logged in successfully',
                'user_id': user.id
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password'
            }, status=401)
            
    except KeyError as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Missing field: {str(e)}'
        }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON in request body'
        }, status=400)

#Logout User
@csrf_exempt
@login_required(login_url='custom_auth/login/')
def logoutUser(request):
    """
    Logs out the currently authenticated user.
    
    This view handles user logout requests. If the user is authenticated,
    they are logged out of the system. The view returns a success response
    regardless of whether a user was actually logged in.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        JsonResponse: A JSON response indicating the success of the logout operation.
        
    Notes:
        - The @login_required decorator ensures that only authenticated users can access this view.
        - If an unauthenticated user attempts to access this view, they are redirected to the login page.
    """
    logout(request)
    return JsonResponse({
        'status': 'success',
        'message': 'User logged out successfully'
    })

#Change Password
@csrf_exempt
@login_required(login_url='custom_auth/login/')
def changePassword(request):
    """
    Changes the password for the currently authenticated user.
    
    This view processes POST requests containing the current password and a new password.
    It verifies that the current password is correct before updating to the new password.
    
    Args:
        request (HttpRequest): The HTTP request object containing password data.
        
    Returns:
        JsonResponse: A JSON response indicating the success or failure of the password change.
        
    Raises:
        KeyError: If any required field is missing from the request data.
        
    Notes:
        - The @login_required decorator ensures that only authenticated users can access this view.
        - The request method must be POST.
        - The request body must contain 'current_password' and 'new_password' fields.
        - The current password is verified before changing to the new password.
        - If the current password is incorrect, an error response is returned.
    """
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        })
        
    try:
        data = json.loads(request.body)
        current_password = data['current_password']
        new_password = data['new_password']
        
        # Verify current password
        user = request.user
        if not user.check_password(current_password):
            return JsonResponse({
                'status': 'error',
                'message': 'Current password is incorrect'
            }, status=400)
            
        # Set and hash the new password
        user.set_password(new_password)
        user.save()
        
        # Re-authenticate the user with the new password
        login(request, user)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Password changed successfully'
        })
        
    except KeyError as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Missing field: {str(e)}'
        }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON in request body'
        }, status=400)