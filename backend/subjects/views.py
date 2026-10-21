from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError
from .models import Subject
from .serializers import SubjectSerializer

class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all().order_by("name")
    serializer_class = SubjectSerializer

class SubjectUpdateView(generics.UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = "id"
    def put(self, request, *args, **kwargs):
        self.kwargs["id"] = request.data.get("id")
        return super().put(request, *args, **kwargs)

class SubjectDeleteView(generics.DestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response({"message": "This subject has attendance records and cannot be deleted."}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)
