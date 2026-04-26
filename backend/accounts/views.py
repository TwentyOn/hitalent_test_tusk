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
        data = request.data
        print(data)
        data['activation_key'] = 'test_key'
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
