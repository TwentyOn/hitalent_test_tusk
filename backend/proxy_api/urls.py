from django.urls import path
from .views import ActivateKeyView

urlpatterns = [
    path('activate-key/', ActivateKeyView.as_view())
]