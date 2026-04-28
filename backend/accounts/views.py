from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .serializers import UserSerializer


# Create your views here.
class UserView(GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        if not request.user.is_authenticated:
            raise AuthenticationFailed('Требуется аунтетификация')

        user = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    def partial_update(self, request, pk):
        if not request.user.is_authenticated:
            raise AuthenticationFailed('Требуется аунтетификация')

        user = get_object_or_404(User, pk=pk)
        user.activation_key = user.create_activation_key()
        user.save()

        return Response({'activation_key': user.activation_key})
