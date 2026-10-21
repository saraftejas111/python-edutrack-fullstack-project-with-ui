from rest_framework import serializers
from .models import AttendanceSession

class AttendanceSessionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    numberOfStudents = serializers.SerializerMethodField()
    class Meta:
        model = AttendanceSession
        fields = ("id", "date", "time", "numberOfStudents", "user", "subject", "students")
    def get_user(self, obj):
        return {"username": obj.faculty.username, "firstName": obj.faculty.first_name, "lastName": obj.faculty.last_name}
    def get_subject(self, obj):
        return {"id": obj.subject_id, "name": obj.subject.name}
    def get_students(self, obj):
        return [{"id": entry.student_id, "name": entry.student.name} for entry in obj.entries.all() if entry.status == "present"]
    def get_numberOfStudents(self, obj):
        return sum(1 for entry in obj.entries.all() if entry.status == "present")

class TakeAttendanceSerializer(serializers.Serializer):
    username = serializers.CharField()
    subjectId = serializers.IntegerField(min_value=1)
    date = serializers.DateField()
    time = serializers.TimeField()
    students = serializers.ListField(child=serializers.DictField(), allow_empty=True)
