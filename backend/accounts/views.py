from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer
from .tasks import send_activation_key
from .permissions import UserOwnerPermission


# Create your views here.
class UserView(GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'change_password', 'logout'):
            return [UserOwnerPermission()]
        return [permissions.AllowAny()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='change-password', serializer_class=ChangePasswordSerializer)
    def change_password(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'user': user})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'успех'})


class ActivationKeyView(APIView):
    permission_classes = [UserOwnerPermission]
    serializer_class = None

    @extend_schema(responses={
        404: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string', 'default': 'описание ошибки'}
                }
            },
            description='Ошибка поиска пользователя по ID'
        ),
        200: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'activation_key': {'type': 'string', 'default': 'новый ключ активации'}
                }
            }
        )
    })
    def post(self, request, id):
        """
        Обновление ключа пользователя
        """
        user = get_object_or_404(User, pk=id)

        activation_key = user.create_activation_key()
        user.activation_key = activation_key
        user.save()

        send_activation_key.delay(user.email, activation_key)

        return Response({'activation_key': activation_key})
