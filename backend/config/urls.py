from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("users.urls")),
    path("student/", include("students.urls")),
    path("subject/", include("subjects.urls")),
    path("attendance/", include("attendance.urls")),
]
