from django.db import models
from django.db.models import Max

from .const import Gender


class Citizen(models.Model):
    citizen_id = models.PositiveIntegerField(verbose_name='id гражданина')
    import_id = models.PositiveIntegerField(verbose_name='id импорт')
    town = models.CharField(max_length=256, verbose_name='Название города')
    street = models.CharField(max_length=256, verbose_name='Название улицы')
    building = models.CharField(max_length=256, verbose_name='Номер дома, корпус, строение')
    apartment = models.PositiveIntegerField(verbose_name='Номер квартиры')
    name = models.CharField(max_length=256, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения')
    gender = models.CharField(verbose_name='Пол', max_length=6, choices=Gender.choices)
    relatives = models.ManyToManyField('Citizen', verbose_name='Ближайшие родственники', symmetrical=True)

    @staticmethod
    def max_import_id():
        max_import_id = Citizen.objects.aggregate(Max('import_id'))['import_id__max']
        return max_import_id + 1 if max_import_id else 1
