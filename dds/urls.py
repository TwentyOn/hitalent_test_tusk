from django.urls import path
from .views import DdsListView, DdsCreateView, DdsDetailView

urlpatterns = [
    path('dds/', DdsListView.as_view(), name='dds-list'),
    path('dds/<int:id>/detail/', DdsDetailView.as_view(), name='dds-detail'),
    path('dds/create/', DdsCreateView.as_view(), name='dds-create'),
]