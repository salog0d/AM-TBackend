from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register_user'),
    path('delete/<int:custom_user_id>/', views.deleteUser, name='delete_user'),
    path('update/<int:custom_user_id>/', views.updateUser, name='update_user'),
    path('get/<int:custom_user_id>/', views.getUser, name='get_user'),
    path('list/', views.listUsers, name='list_users'),
    path('login/', views.UserLoginView.as_view(), name='login_user'), 
    path('logout/', views.logoutUser, name='logout_user'),
    
]