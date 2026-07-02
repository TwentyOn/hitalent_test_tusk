from django.urls import path

from .views import MainView, StatusCreateView, TypeCreateView, CategoryCreateView

app_name = 'dictionary'

urlpatterns = [
    path('', MainView.as_view(), name='manage'),
    path('status/create/', StatusCreateView.as_view(), name='status-create'),
    path('type/create/', TypeCreateView.as_view(), name='type-create'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
]