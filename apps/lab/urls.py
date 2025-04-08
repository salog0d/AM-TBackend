from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createTest, name='create_test'),
    path('list/', views.viewTests, name='view_tests'),
    path('delete/<int:test_id>/', views.deleteTest, name='delete_test'),
    path('update/<int:test_id>/', views.updateTest, name='update_test'),
    path('view/<int:test_id>/', views.viewTest, name='view_test'),
]