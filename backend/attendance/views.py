from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from students.models import Student
from subjects.models import Subject
from .models import AttendanceEntry, AttendanceSession
from .serializers import AttendanceSessionSerializer, TakeAttendanceSerializer

def records():
    return AttendanceSession.objects.select_related("faculty", "subject").prefetch_related("entries__student")

class TakeAttendanceView(APIView):
    def post(self, request):
        serializer = TakeAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        faculty = get_object_or_404(User, username=data["username"], role=User.Role.FACULTY)
        subject = get_object_or_404(Subject, pk=data["subjectId"])
        raw_ids = [item.get("id") for item in data["students"]]
        if any(not isinstance(pk, int) for pk in raw_ids) or len(set(raw_ids)) != len(raw_ids):
            raise ValidationError({"students": "Provide unique integer student IDs."})
        student_ids = set(raw_ids)
        students = list(Student.objects.all().order_by("id"))
        known_ids = {student.id for student in students}
        unknown = student_ids - known_ids
        if unknown:
            raise ValidationError({"students": f"Unknown student IDs: {sorted(unknown)}"})
        if not students:
            raise ValidationError({"students": "Add students before taking attendance."})
        with transaction.atomic():
            session = AttendanceSession.objects.create(faculty=faculty, subject=subject, date=data["date"], time=data["time"])
            AttendanceEntry.objects.bulk_create([
                AttendanceEntry(session=session, student=student,
                                status=AttendanceEntry.Status.PRESENT if student.id in student_ids else AttendanceEntry.Status.ABSENT)
                for student in students
            ])
        return Response(AttendanceSessionSerializer(records().get(pk=session.pk)).data, status=status.HTTP_201_CREATED)

class AttendanceListView(APIView):
    def get(self, request):
        queryset = records()
        page = self.paginate_queryset(queryset, request)
        return self.get_paginated_response(AttendanceSessionSerializer(page, many=True).data)
    def paginate_queryset(self, queryset, request):
        from rest_framework.pagination import PageNumberPagination
        self.paginator = PageNumberPagination()
        self.paginator.page_size = 50
        return self.paginator.paginate_queryset(queryset, request, view=self)
    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)

class FilteredAttendanceView(APIView):
    def get(self, request, faculty_username, subject_id, date):
        faculty = get_object_or_404(User, username=faculty_username)
        queryset = records().filter(faculty=faculty, subject_id=subject_id, date=date)
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 50
        page = paginator.paginate_queryset(queryset, request, view=self)
        return paginator.get_paginated_response(AttendanceSessionSerializer(page, many=True).data)
