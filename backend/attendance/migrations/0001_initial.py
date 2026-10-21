import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("students", "0001_initial"),
        ("subjects", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="AttendanceSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(db_index=True)),
                ("time", models.TimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("faculty", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="attendance_sessions", to=settings.AUTH_USER_MODEL)),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="attendance_sessions", to="subjects.subject")),
            ],
            options={"ordering": ("-date", "-time", "-id")},
        ),
        migrations.CreateModel(
            name="AttendanceEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("present", "Present"), ("absent", "Absent")], max_length=7)),
                ("session", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="entries", to="attendance.attendancesession")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="attendance_entries", to="students.student")),
            ],
        ),
        migrations.AddConstraint(
            model_name="attendanceentry",
            constraint=models.UniqueConstraint(fields=("session", "student"), name="unique_student_per_attendance_session"),
        ),
    ]
