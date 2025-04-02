from django.urls import path
from . import views

urlpatterns = [
    path("login/", views),
    path("createUser/", views.createUser, name="createUser"),
    path("deleteUser/", views.deleteUser, name="deleteUser"),
    path("updateUser/", views.updateUser, name="updateUser"),
    path("getUser/", views.getUser, name="getUser"),
    path("listUsers/", views.listUsers, name="listUsers"),
    path("loginUser/", views.loginUser, name="loginUser"),
    path("logoutUser/", views.logoutUser, name="logoutUser"),
    path("changePassword/", views.changePassword, name="changePassword"),
]   