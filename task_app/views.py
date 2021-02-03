from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializer import CitizenSerializer


class CreateImports(APIView):
    def post(self, request):
        serializer = CitizenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response({'data': {'import_id': data}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



