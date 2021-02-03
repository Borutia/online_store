from rest_framework import serializers
from datetime import datetime

from .const import Gender
from .models import Citizen


class CitizenSerializer(serializers.Serializer):
    citizen_id = serializers.IntegerField(min_value=1)
    town = serializers.CharField(max_length=256)
    street = serializers.CharField(max_length=256)
    building = serializers.CharField(max_length=256)
    apartment = serializers.IntegerField(min_value=1)
    name = serializers.CharField(max_length=256)
    birth_date = serializers.DateField()
    gender = serializers.ChoiceField(choices=Gender.choices)
    relatives = serializers.ListField()

    # def validate_birth_date(self, birth_date):
    #     if datetime.now() < birth_date:
    #         raise serializers.ValidationError('Bad birth_date')

    def create(self, validated_data):
        return Citizen.objects.create(**validated_data)
