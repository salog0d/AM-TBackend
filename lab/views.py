import json
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required
from lab.models import Test

# All views here ar just for the admin user type
@login_required(login_url='custom_user/login/')
def createTest(request):
    """
This view is restricted to superusers and only accepts POST requests with 
JSON payload. It processes the request to create a new test instance in the 
database.
Parameters:
    request (HttpRequest): The HTTP request object containing user information 
    and request data.
Returns:
    JsonResponse: 
        - On success: A JSON response with a success message and HTTP 201 status.
        - On failure: A JSON response with an error message and appropriate 
          HTTP status code:
            - 403: If the user is not a superuser.
            - 400: If the request method is not POST or the JSON data is invalid.
Raises:
    json.JSONDecodeError: If the request body contains invalid JSON data.
    """
    if not request.user.is_superuser:
        return JsonResponse({"error": "No permission to create test"}, status=403)

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        test_name = data.get('name')
        test_description = data.get('description')
        test_unit = data.get('unit')
        test_category = data.get('category')
        higher_is_better = data.get('higher_is_better')

        new_test = Test(
            name=test_name,
            description=test_description,
            unit=test_unit,
            category=test_category,
            higher_is_better=higher_is_better
        )
        new_test.save()

        return JsonResponse({"success": "Test created successfully"}, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)



@login_required(login_url='custom_user/login/')
def deleteTest(request, test_id):
    """
This view function allows a superuser or an admin user to delete a test 
identified by its `test_id`. If the user does not have the required 
permissions, a JSON response with an error message and a 403 status code 
is returned.
Parameters:
    request (HttpRequest): The HTTP request object containing metadata 
        about the request.
    test_id (int): The ID of the test to be deleted.
Returns:
    JsonResponse: A JSON response indicating the success or failure of 
        the deletion operation. On success, a 200 status code is returned 
        with a success message. On failure due to insufficient permissions, 
        a 403 status code is returned with an error message.
Permissions:
    - The user must be a superuser or have admin privileges to delete a test.
    """
    if request.user.is_superuser or request.user.is_admin():
        test = Test.objects.filter(id=test_id)
        test.delete()
        return JsonResponse({"success": "Test deleted successfully"}, status=200)
    else:
        
        return JsonResponse({"error": "No permission to delete test"}, status=403)


@login_required(login_url='custom_user/login/')
def updateTest(request, test_id):
    """
    This view function allows authorized users to update the details of a specific test.
    It ensures that only superusers or users with admin privileges can perform the update.
    The function expects a POST request with a JSON payload containing the updated test details.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        test_id (int): The ID of the test to be updated.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the update operation.
            - On success: Returns a JSON object with a success message and HTTP status 200.
            - On failure: Returns a JSON object with an error message and appropriate HTTP status:
                - 403 if the user lacks permissions.
                - 400 if the request method is not POST or the JSON data is invalid.

    Raises:
        Test.DoesNotExist: If no test with the given ID exists in the database.

    Notes:
        - The `request.body` is expected to contain a JSON object with the following keys:
            - `name` (str): The updated name of the test.
            - `description` (str): The updated description of the test.
            - `unit` (str): The unit of measurement for the test.
            - `category` (str): The category to which the test belongs.
            - `higher_is_better` (bool): Indicates whether higher values are better for this test.
        - The user must be authenticated and have the required permissions to perform this action.
        """
    if not request.user.is_superuser and not request.user.is_admin():
        return JsonResponse({"error": "No permission to update test"}, status=403)
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    try:
        data = json.loads(request.body)
        test_name = data.get('name')
        test_description = data.get('description')
        test_unit = data.get('unit')
        test_category = data.get('category')
        higher_is_better = data.get('higher_is_better')

        test = Test.objects.get(id=test_id)
        test.name = test_name
        test.description = test_description
        test.unit = test_unit
        test.category = test_category
        test.higher_is_better = higher_is_better
        test.save()

        return JsonResponse({"success": "Test updated successfully"}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    

@login_required(login_url='custom_user/login/')
def viewTest(request, test_id):
    """
This view function retrieves and returns the details of a test identified by its `test_id`.
It ensures that only superusers or users with admin privileges can access the test details.

Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.
    test_id (int): The unique identifier of the test to be retrieved.

Returns:
    JsonResponse:
        - If the user is authorized and the test exists:
            A JSON response containing the test details with a status code of 200.
        - If the test does not exist:
            A JSON response with an error message and a status code of 404.
        - If the user lacks the necessary permissions:
            A JSON response with an error message and a status code of 403.

Raises:
    None

Notes:
    - The user must be logged in to access this view. If not logged in, they will be redirected
      to the login page specified by `login_url`.
    - The `Test` model is queried to fetch the test details. Ensure the model is properly defined
      and imported.
"""
    if request.user.is_superuser or request.user.is_admin():
        test = Test.objects.filter(id=test_id)
        if test.exists():
            # Render the test details or return as JSON
            test_data = {
                "id": test.id,
                "name": test.name,
                "description": test.description,
                "unit": test.unit,
                "category": test.category,
                "higher_is_better": test.higher_is_better,
            }
            return JsonResponse({"test": test_data}, status=200)
        else:
            return JsonResponse({"error": "Test not found"}, status=404)

    return JsonResponse({"error": "No permission to view test"}, status=403)