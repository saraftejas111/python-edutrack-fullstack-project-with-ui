from django.urls import path
from .views import SubjectDeleteView, SubjectListCreateView, SubjectUpdateView

urlpatterns = [
    path("add-subject/", SubjectListCreateView.as_view()),
    path("get-all-subjects/", SubjectListCreateView.as_view()),
    path("update-subject/", SubjectUpdateView.as_view()),
    path("delete-subject/<int:pk>/", SubjectDeleteView.as_view()),
]
