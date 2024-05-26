from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer


class UserView(viewsets.ModelViewSet):

    serializer_class = UserSerializer

    def get_object(self, request, *args, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(User, pk=item)

    queryset = User.objects.all()

    def list(self, request):
        queryset = User.objects.filter(is_superuser=True)
        serializer_class = self.serializer_class(queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer_class = UserSerializer(user)
        return Response(serializer_class.data)
