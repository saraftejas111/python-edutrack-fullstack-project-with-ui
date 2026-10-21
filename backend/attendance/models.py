from django.conf import settings
from django.db import models

class AttendanceSession(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="attendance_sessions")
    subject = models.ForeignKey("subjects.Subject", on_delete=models.PROTECT, related_name="attendance_sessions")
    date = models.DateField(db_index=True)
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ("-date", "-time", "-id")

class AttendanceEntry(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name="entries")
    student = models.ForeignKey("students.Student", on_delete=models.PROTECT, related_name="attendance_entries")
    status = models.CharField(max_length=7, choices=Status.choices)
    class Meta:
        constraints = [models.UniqueConstraint(fields=("session", "student"), name="unique_student_per_attendance_session")]
