from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from dictionary.models import Status, Category, Type

# Create your views here.
class TypeView(APIView):
    def get(self, request, pk):
        type_obj = Type.objects.get(pk=pk)
        categories = type_obj.category.all()
        response = {c.pk: c.name for c in categories}
        return Response(response)

class CategoryView(APIView):
    def get(self, request, pk):
        category_obj = Category.objects.get(pk=pk)
        types = category_obj.type_set.all()
        response = {type.pk: type.name for type in types}
        print(response)
        return Response(response)