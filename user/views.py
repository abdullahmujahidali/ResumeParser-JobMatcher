from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from user.models import User
from user.serializers import UserSerializer, ResumeSerializer, AccountCreationSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountCreationSerializer
        if self.action == 'uploadResume':
            return ResumeSerializer
        return UserSerializer

    def get_object(self, request, *args, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(User, pk=item)

    def list(self, request):
        queryset = User.objects.filter(is_superuser=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False, methods=["post"],
        name="Upload User Resume", url_path="upload-resume",
        parser_classes=[MultiPartParser, FormParser]
    )
    def uploadResume(self, request, pk=None):
        user = get_object_or_404(User, email=request.data.get("email"))
        my_serializer = ResumeSerializer(user, data=request.data, partial=True)
        if my_serializer.is_valid():
            my_serializer.save()
            return Response({"message": "Resume uploaded successfully"})
        return Response(
            my_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
