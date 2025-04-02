from django.urls import path
from . import views

urlpatterns = [
    path("createUser/", views.createUser, name="createUser"),
    path("deleteUser/<int:custom_user_id>/", views.deleteUser, name="deleteUser"),
    path("updateUser/<int:custom_user_id>/", views.updateUser, name="updateUser"),
    path("getUser/<int:custom_user_id>/", views.getUser, name="getUser"),
    path("listUsers/", views.listUsers, name="listUsers"),
    #path("loginUser/", views.loginUser, name="loginUser"),
    #path("logoutUser/", views.logoutUser, name="logoutUser"),
    #path("changePassword/", views.changePassword, name="changePassword"),
]   