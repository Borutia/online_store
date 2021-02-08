from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializer import *


class Imports(APIView):
    def get(self, request, import_id):
        instances = Citizen.objects.filter(import_id=import_id)
        if len(instances) == 0:
            return Response("unknown id", status=status.HTTP_400_BAD_REQUEST)
        serializer = CitizenGetUpdateSerializer(instances, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CitizenCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response({'data': {'import_id': data}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, import_id, citizen_id):
        if len(request.data) == 0:
            return Response({'error': "Body is empty"}, status=status.HTTP_400_BAD_REQUEST)
        instance = Citizen.objects.get(import_id=import_id, citizen_id=citizen_id)
        serializer = CitizenGetUpdateSerializer(instance, data=request.data, partial=True,
                                                context={'import_id': import_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CitizenBirthdays(APIView):
    def get(self, request, import_id):
        data = {'data': ''}
        serializer = CitizenGiftsSerializer(data, context={'import_id': import_id})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CitizenPercentileAge(APIView):
    def get(self, request, import_id):
        data = {'data': []}
        serializer = CitizenPercentileAgeSerializer(data, context={'import_id': import_id})
        return Response(serializer.data, status=status.HTTP_200_OK)
