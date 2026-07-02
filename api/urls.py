from django.urls import path

from .views import TypeView, CategoryView

urlpatterns = [
    path('dictionary/type/<int:pk>/categories/', TypeView.as_view()),
    path('dictionary/category/<int:pk>/types/', CategoryView.as_view()),
]