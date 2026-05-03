from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
from rest_framework.routers import DefaultRouter

from .views import UserView, ActivationKeyView

router = DefaultRouter()
router.register(prefix='', viewset=UserView)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view()),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('<int:id>/update-key/', ActivationKeyView.as_view())
] + router.urls
