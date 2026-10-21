from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError
from .models import Student
from .serializers import StudentSerializer

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all().order_by("id")
    serializer_class = StudentSerializer

class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"
    def put(self, request, *args, **kwargs):
        self.kwargs["id"] = request.data.get("id")
        return super().put(request, *args, **kwargs)

class StudentDeleteView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response({"message": "This student has attendance records and cannot be deleted."}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)
