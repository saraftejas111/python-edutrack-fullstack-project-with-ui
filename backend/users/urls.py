from django.urls import path
from .views import FacultyListView, LoginView, RegisterUserView, UserDeleteView, UserDetailView, UserListView, UserUpdateView

urlpatterns = [
    path("login-user/", LoginView.as_view()),
    path("register-user/", RegisterUserView.as_view()),
    path("get-all-user/", UserListView.as_view()),
    path("get-all-faculty/", FacultyListView.as_view()),
    path("get-user-by-username/<str:username>/", UserDetailView.as_view()),
    path("update-user/", UserUpdateView.as_view()),
    path("delete-user-by-username", UserDeleteView.as_view()),
]
