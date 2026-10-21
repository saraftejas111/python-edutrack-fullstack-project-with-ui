from django.urls import path
from .views import StudentDeleteView, StudentListCreateView, StudentUpdateView

urlpatterns = [
    path("add-student/", StudentListCreateView.as_view()),
    path("get-all-students/", StudentListCreateView.as_view()),
    path("update-student/", StudentUpdateView.as_view()),
    path("delete-student/<int:pk>/", StudentDeleteView.as_view()),
]
