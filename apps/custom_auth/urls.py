
from django.urls import path
from . import views

urlpatterns = [
    # Rutas de autenticación JWT
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'), 
    # Rutas de usuarios
    path('register/', views.UserRegistrationView.as_view(), name='register_user'),
    path('profile/', views.getUserProfile, name='user_profile'),
    path('delete/<int:custom_user_id>/', views.deleteUser, name='delete_user'),
    path('update/<int:custom_user_id>/', views.updateUser, name='update_user'),
    path('get/<int:custom_user_id>/', views.getUser, name='get_user'),
    path('list/', views.listUsers, name='list_users'),
    path("logout/", views.logoutUser, name="logout-user"),
]