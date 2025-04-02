from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from custom_auth.models import CustomUser

"""

This section contains the different views for the dashboard
These views are responsible for rendering the admin dashboard and managing user data.

The views include:
- admin_dashboard: Renders the admin dashboard and retrieves all users in the system.
- coach_dashboard: Renders the coach dashboard and retrieves all athletes associated with a specific coach.
- athlete_dashboard: Renders the athlete dashboard and retrieves the details of a specific athlete.

"""
@login_required(login_url='custom_auth/login/')  # Ensure the user is logged in before accessing this view
def adminDashboard(request):
    """
    Render the admin dashboard.

    This view retrieves all users in the system and returns their details.
    It ensures that the requesting user is authenticated and has the role of admin.
    """
    # Check if the user is authenticated and has an admin role
    if request.user.is_authenticated and request.user.is_admin():
        try:
            # Retrieve all users in the system and serialize their details
            users = list(CustomUser.objects.values(
                'id', 'username', 'name', 'email', 'role', 'discipline', 'date_of_birth', 'phone_number'
            ))

            # Return a success response with the list of users
            return JsonResponse({
                'status': 'success',
                'users': users
            })
        except CustomUser.DoesNotExist:  # Handle the case where no users are found
            return JsonResponse({
                'status': 'error',
                'message': 'No users found'
            }, status=404)
    else:
        # Return a permission error if the user is not authorized to access this view
        return JsonResponse({
            'status': 'error',
            'message': 'No permission to view this page'
        }, status=403)


# Dashboard to see athletes associated with a coach
@login_required(login_url='custom_auth/login/')  # Ensure the user is logged in before accessing this view
def coachDashboard(request, custom_user_id):
    """
    Render the coach dashboard.

    This view retrieves all athletes associated with a specific coach. 
    It ensures that the requesting user is authenticated and has the role of a coach.
    """
    if request.user.is_authenticated and request.user.is_coach():  # Check if the user is authenticated and has a coach role
        try:
            # Retrieve the coach user object based on the provided ID and role
            coach = CustomUser.objects.get(id=custom_user_id, role='coach')
            
            # Fetch all athletes associated with the coach and serialize their details
            athletes = list(coach.athletes.all().values(
                'id', 'username', 'name', 'email', 'discipline', 'date_of_birth', 'phone_number'
            ))
            
            # Return a success response with the list of athletes
            return JsonResponse({
                'status': 'success',
                'athletes': athletes
            })
        except CustomUser.DoesNotExist:  # Handle the case where the coach does not exist
            return JsonResponse({
                'status': 'error',
                'message': 'Coach not found'
            }, status=404)
    else:
        # Return a permission error if the user is not authorized to access this view
        return JsonResponse({
            'status': 'error',
            'message': 'No permission to view this page'
        }, status=403)


#Athlete
def athleteDashboard(request, custom_user_id):
    """
    Render the athlete dashboard.
    This view retrieves the details of a specific athlete.
    It ensures that the requesting user is authenticated and has the role of athlete.
    """

    if request.user.is_authenticated and request.user.is_athlete():
        try:
            # Retrieve the athlete user object based on the provided ID and role
            athlete = CustomUser.objects.get(id=custom_user_id, role='athlete')
            
            # Serialize the athlete's details
            athlete_data = {
                'id': athlete.id,
                'username': athlete.username,
                'name': athlete.name,
                'email': athlete.email,
                'discipline': athlete.discipline,
                'date_of_birth': athlete.date_of_birth,
                'phone_number': athlete.phone_number
            }
            # Return a success response with the athlete's details
            return JsonResponse({
                'status': 'success',
                'athlete': athlete_data
            })
        except CustomUser.DoesNotExist:  # Handle the case where the athlete does not exist
            return JsonResponse({
                'status': 'error',
                'message': 'Athlete not found'
            }, status=404)
    else:
        # Return a permission error if the user is not authorized to access this view
        return JsonResponse({
            'status': 'error',
            'message': 'No permission to view this page'
        })
    
"""

This section contains the defferent views for details from the dashboard
These views are responsible for rendering the details of the dashboard and managing user data.
The views include:

"""

@login_required(login_url='custom_auth/login/')  # Ensure the user is logged in before accessing this view
def userDetails(request, custom_user_id):
    """
    Render the user details.

    This view retrieves the details of a specific user based on their ID.
    It ensures that the requesting user is authenticated and has the appropriate role.
    """
    if request.user.is_authenticated and request.user.is_admin():
        try:
            # Retrieve the user object based on the provided ID
            user = CustomUser.objects.get(id=custom_user_id)
            
            # Serialize the user's details
            user_data = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'discipline': user.discipline,
                'date_of_birth': user.date_of_birth,
                'phone_number': user.phone_number
            }
            
            # Return a success response with the user's details
            return JsonResponse({
                'status': 'success',
                'user': user_data
            })
        except CustomUser.DoesNotExist:  # Handle the case where the user does not exist
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            }, status=404)
    else:
        # Return a permission error if the user is not authorized to access this view
        return JsonResponse({
            'status': 'error',
            'message': 'No permission to view this page'
        }, status=403)
    

@login_required(login_url='custom_auth/login/') 
def athleteDetails(request, custom_user_id):
    """"
    Render the athlete details.
    This view retrieves the details of a specific athlete based on their ID.
    It ensures that the requesting user is authenticated and has the appropriate role.
    """
    if request.user.is_authenticated and request.user.is_coach():
        try:
            # Retrieve the athlete user object based on the provided ID and role
            athlete = CustomUser.objects.get(id=custom_user_id, role='athlete')
            
            # Serialize the athlete's details
            athlete_data = {
                'id': athlete.id,
                'username': athlete.username,
                'name': athlete.name,
                'email': athlete.email,
                'discipline': athlete.discipline,
                'date_of_birth': athlete.date_of_birth,
                'phone_number': athlete.phone_number
            }
            # Return a success response with the athlete's details
            return JsonResponse({
                'status': 'success',
                'athlete': athlete_data
            })
        except CustomUser.DoesNotExist:  # Handle the case where the athlete does not exist
            return JsonResponse({
                'status': 'error',
                'message': 'Athlete not found'
            }, status=404)
    else:
        # Return a permission error if the user is not authorized to access this view
        return JsonResponse({
            'status': 'error',
            'message': 'No permission to view this page'
        }, status=403)

"""

This section contains the different views for the tests appearing for each athlete
These views are responsible for rendering the tests and managing user data.
The views include:
- test_results: Renders the test results for a specific athlete.

"""

@login_required(login_url='custom_auth/login/')  # Ensure the user is logged in before accessing this view
def testResults(request, custom_user_id):
    """
    Render the test results for a specific athlete.

    This view retrieves the test results associated with a specific athlete.
    It ensures that the requesting user is authenticated and has the appropriate role 
    (admin, coach, or the athlete themselves) to access the data.
    """
    # Retrieve the athlete object based on the provided ID and role, or return a 404 if not found
    athlete = get_object_or_404(CustomUser, id=custom_user_id, role='athlete')

    # Check the role of the requesting user and validate permissions
    if request.user.is_admin():
        # Admins can access test results for all athletes
        pass
    elif request.user.is_coach():
        # Coaches can only access test results for athletes they are associated with
        if athlete.coach != request.user:
            return JsonResponse({
                'status': 'error',
                'message': 'No permission to view this athlete'
            }, status=403)
    else:
        # Return a permission error if the user is neither an admin nor a coach
        return JsonResponse({
            'status': 'error',
            'message': 'No permission to view this page'
        }, status=403)

    # Retrieve and serialize the test results for the athlete
    test_results = list(athlete.test_results.values(
        'id', 'athlete', 'test', 'session', 'numeric_value', 'notes', 'date_recorded'
    ))

    # Return a success response with the test results
    return JsonResponse({
        'status': 'success',
        'test_results': test_results
    })
