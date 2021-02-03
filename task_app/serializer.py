from rest_framework import serializers
from datetime import datetime

from .models import Citizen


class BaseCitizenSerializer(serializers.ModelSerializer):
    relatives = serializers.ListField()

    class Meta:
        model = Citizen
        fields = ('citizen_id', 'town', 'street', 'building',
                  'apartment', 'name', 'birth_date', 'gender', 'relatives')

    def validate_birth_date(self, date):
        if datetime.now().date() < date:
            raise serializers.ValidationError('Error date')
        return date


class CitizenSerializer(serializers.ModelSerializer):
    citizens = BaseCitizenSerializer(many=True)

    class Meta:
        model = Citizen
        fields = ["citizens"]

    def validate(self, data):
        for citizen in data['citizens']:
            current_relatives = citizen.get('relatives')
            if citizen['citizen_id'] in current_relatives:
                raise serializers.ValidationError('Error relatives')
            if current_relatives:
                for other_citizen in data['citizens']:
                    if other_citizen['citizen_id'] is not citizen['citizen_id']:
                        for current_relative in current_relatives:
                            if current_relative is other_citizen['citizen_id']:
                                other_relatives = other_citizen.get('relatives')
                                if other_relatives:
                                    if citizen['citizen_id'] not in other_relatives:
                                        raise serializers.ValidationError('Error relatives')
                                else:
                                    raise serializers.ValidationError('Error relatives')
        return data

    def create(self, validated_data):
        max_import_id = Citizen.max_import_id()
        relatives = []
        for citizen in validated_data['citizens']:
            citizen['import_id'] = max_import_id
            relatives.append(
                {
                    citizen['citizen_id']: citizen.pop('relatives')
                }
            )
            Citizen.objects.create(**citizen)
        for relative in relatives:
            for citizen_id, current_relatives in relative.items():
                instance = Citizen.objects.filter(citizen_id=citizen_id, import_id=max_import_id).first()
                instances_relatives = Citizen.objects.filter(citizen_id__in=current_relatives,
                                                             import_id=max_import_id).all()
                instance.relatives.add(*instances_relatives)
        return max_import_id