from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class Test(APIView):
    def post(self, request):
        print(request.data)
        return Response({'message': 'ok'})



