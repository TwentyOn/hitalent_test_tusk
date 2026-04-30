from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .serializers import UserSerializer
from .tasks import send_activation_key


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


class ActivationKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """
        Обновление ключа пользователя
        :param request:
        :return:
        """
        user = get_object_or_404(User, pk=user_id)
        user.activation_key = user.create_activation_key()
        user.save()

        send_activation_key.delay(user.email, user.activation_key)

        return Response({'message': 'успех'})
