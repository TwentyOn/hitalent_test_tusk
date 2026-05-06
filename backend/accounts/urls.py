from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.routers import DefaultRouter

from .views import UserView, UpdateKeyView

router = DefaultRouter()
router.register(prefix='', viewset=UserView)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view()),
    path('<int:pk>/update-key/', UpdateKeyView.as_view(), name='user-update-key')
] + router.urls
