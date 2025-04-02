from django.urls import path
from . import views

urlpatterns = [
    path("adminDashboard/", views.adminDashboard, name="adminDashboard"),
    path("athleteDashboard/<int:custom_user_id>/", views.athleteDashboard, name="athleteDashboard"),
    path("coachDashboard/", views.coachDashboard, name="coachDashboard"),
    path("userDetails/<int:custom_user_id>/", views.userDetails, name="userDetails"),
    path("athleteDetails/<int:custom_user_id>/", views.athleteDetails, name="athleteDetails"),
    path("testResults/<int:custom_user_id>/", views.testResults, name="testResults"),
]