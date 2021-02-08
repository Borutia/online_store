import numpy as np

from rest_framework import serializers
from datetime import datetime

from .models import Citizen
from .const import Gender
from .utils import calculate_age


class BaseCitizenSerializer(serializers.ModelSerializer):
    citizen_id = serializers.IntegerField(min_value=1)
    town = serializers.CharField(max_length=256)
    street = serializers.CharField(max_length=256)
    building = serializers.CharField(max_length=256)
    apartment = serializers.IntegerField(min_value=1)
    name = serializers.CharField(max_length=256)
    gender = serializers.ChoiceField(choices=Gender.choices)
    relatives = serializers.ListField()

    class Meta:
        model = Citizen
        fields = ('citizen_id', 'town', 'street', 'building',
                  'apartment', 'name', 'birth_date', 'gender', 'relatives',)

    def validate_birth_date(self, date):
        if datetime.now().date() < date:
            raise serializers.ValidationError('Error date')
        return date


class CitizenCreateSerializer(serializers.ModelSerializer):
    citizens = BaseCitizenSerializer(many=True)

    class Meta:
        model = Citizen
        fields = ("citizens",)

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


class MySlugRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        return Citizen.objects.filter(import_id=self.context['import_id'])


class CitizenGetUpdateSerializer(BaseCitizenSerializer):
    relatives = MySlugRelatedField(many=True, slug_field='citizen_id')

    class Meta:
        model = Citizen
        fields = ('citizen_id', 'town', 'street', 'building', 'apartment',
                  'name', 'birth_date', 'gender', 'relatives',)
        read_only_fields = ('citizen_id',)


class CitizenGiftsSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Citizen
        fields = ('data',)

    def get_data(self, obj):
        import_id = self.context['import_id']
        instance = Citizen.objects.filter(import_id=import_id).order_by('citizen_id')
        if len(instance) == 0:
            raise serializers.ValidationError(f'Import id:{import_id} doesnt exist')
        dct = {}
        for num in range(1, 13):
            dct[f'{num}'] = []
        for data in instance:
            citizen_dct = {}
            for relative in data.relatives.all():
                month = f'{relative.birth_date.month}'
                if month not in citizen_dct:
                    citizen_dct[month] = 1
                else:
                    citizen_dct[month] += 1
            for field in citizen_dct.keys():
                dct[field].append({'citizen_id': data.citizen_id, 'presents': citizen_dct[field]})
        return dct


class CitizenPercentileAgeSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Citizen
        fields = ('data',)

    def get_data(self, obj):
        import_id = self.context['import_id']
        instance = Citizen.objects.filter(import_id=import_id)
        if len(instance) == 0:
            raise serializers.ValidationError(f'Import id:{import_id} doesnt exist')
        dct = {}
        for data in instance:
            if data.town not in dct:
                dct[data.town] = []
            dct[data.town].append(calculate_age(data.birth_date))
        cities = []
        for key, item in dct.items():
            a = np.array(item)
            cities.append({
                'town': key,
                "p50": round(np.percentile(a, 50), 2),
                "p75": round(np.percentile(a, 75), 2),
                "p99": round(np.percentile(a, 99), 2)
            })
        return cities
