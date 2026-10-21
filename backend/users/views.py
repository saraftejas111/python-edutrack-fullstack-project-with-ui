from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import LoginSerializer, UserSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response({"username": user.username, "role": user.role})

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer

class FacultyListView(generics.ListAPIView):
    queryset = User.objects.filter(role=User.Role.FACULTY).order_by("first_name", "last_name")
    serializer_class = UserSerializer

class UserDetailView(APIView):
    def get(self, request, username):
        return Response(UserSerializer(get_object_or_404(User, username=username)).data)

class UserUpdateView(APIView):
    def put(self, request):
        username = request.data.get("username")
        if not username:
            return Response({"username": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserDeleteView(APIView):
    def delete(self, request):
        user = get_object_or_404(User, username=request.query_params.get("username"))
        try:
            user.delete()
        except ProtectedError:
            return Response({"message": "This user has attendance records and cannot be deleted."}, status=409)
        return Response(status=status.HTTP_204_NO_CONTENT)
