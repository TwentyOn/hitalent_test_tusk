from django.urls import path
from .views import DdsListView, DdsCreateView, DdsUpdateView, DdsDeleteView

app_name = 'dds'

urlpatterns = [
    path('', DdsListView.as_view(), name='dds-list'),
    path('create/', DdsCreateView.as_view(), name='dds-create'),
    path('<int:id>/update/', DdsUpdateView.as_view(), name='dds-update'),
    path('<int:id>/delete/', DdsDeleteView.as_view(), name='dds-delete'),
]