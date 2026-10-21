from django.urls import path
from .views import AttendanceListView, FilteredAttendanceView, TakeAttendanceView

urlpatterns = [
    path("take-attendance/", TakeAttendanceView.as_view()),
    path("get-all-attendance-records/", AttendanceListView.as_view()),
    path("get-attendance/<str:faculty_username>/<int:subject_id>/<str:date>", FilteredAttendanceView.as_view()),
    path("get-attendance/<str:faculty_username>/<int:subject_id>/<str:date>/", FilteredAttendanceView.as_view()),
]
