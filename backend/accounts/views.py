from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


# Create your views here.
class CreateUserView(GenericAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def post(self, request):
        pass
