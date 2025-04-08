from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createUser, name='create_user'),
    path('delete/<int:custom_user_id>/', views.deleteUser, name='delete_user'),
    path('update/<int:custom_user_id>/', views.updateUser, name='update_user'),
    path('get/<int:custom_user_id>/', views.getUser, name='get_user'),
    path('list/', views.listUsers, name='list_users'),
    path('login/', views.loginUser, name='login_user'),
    path('logout/', views.logoutUser, name='logout_user'),
    path('change-password/', views.changePassword, name='change_password'),
]