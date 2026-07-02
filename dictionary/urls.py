from django.urls import path

from .views import MainView, StatusCreateView, StatusUpdateView, StatusDeleteView, \
    TypeCreateView, TypeUpdateView, TypeDeleteView, \
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name = 'dictionary'

urlpatterns = [
    path('', MainView.as_view(), name='manage'),
    path('status/create/', StatusCreateView.as_view(), name='status-create'),
    path('status/<int:pk>/update/', StatusUpdateView.as_view(), name='status-update'),
    path('status/<int:pk>/delete/', StatusDeleteView.as_view(), name='status-delete'),
    path('type/create/', TypeCreateView.as_view(), name='type-create'),
    path('type/<int:pk>/update/', TypeUpdateView.as_view(), name='type-update'),
    path('type/<int:pk>/delete/', TypeDeleteView.as_view(), name='type-delete'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

]
