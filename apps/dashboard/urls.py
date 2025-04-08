from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.adminDashboard, name='admin_dashboard'),
    path('coach-dashboard/<int:custom_user_id>/', views.coachDashboard, name='coach_dashboard'),
    path('athlete-dashboard/<int:custom_user_id>/', views.athleteDashboard, name='athlete_dashboard'),
    path('athlete-details/<int:custom_user_id>/', views.athleteDetails, name='athlete_details'),
    path('test-results/<int:custom_user_id>/', views.testResults, name='test_results'),
]