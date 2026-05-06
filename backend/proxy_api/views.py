from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ActivateVmSerializer


# Create your views here.
class ActivateKeyView(APIView):
    serializer_class = ActivateVmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
