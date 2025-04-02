from django.urls import path
from . import views

urlpatterns = [
    path("createTest/", views.createTest, name="createTest"),
    path("deleteTest/<int:test_id>/", views.deleteTest, name="deleteTest"),
    path("updateTest/<int:test_id>/", views.updateTest, name="updateTest"),
    path("viewTest/<int:test_id>/", views.viewTest, name="viewTest"),
]