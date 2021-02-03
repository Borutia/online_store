import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Citizen
from .tools import convert_date, validate_date, DateError


@csrf_exempt
@require_http_methods('POST')
def import_create(request):
    data = json.loads(request.body)
    max_import_id = Citizen.max_import_id()
    relatives = []
    for citizen in data['citizens']:
        try:
            current_relatives = citizen.get('relatives')
            if citizen['citizen_id'] in current_relatives:
                raise ValidationError('error relatives')
            if current_relatives:
                for other_citizen in data['citizens']:
                    if other_citizen['citizen_id'] is not citizen['citizen_id']:
                        for current_relative in current_relatives:
                            if current_relative is other_citizen['citizen_id']:
                                other_relatives = other_citizen.get('relatives')
                                if other_relatives:
                                    if citizen['citizen_id'] not in other_relatives:
                                        raise ValidationError('error relatives')
                                else:
                                    raise ValidationError('error relatives')
        except ValidationError:
            return HttpResponse(status=400)
    for citizen in data['citizens']:
        try:
            date = convert_date(citizen['birth_date'])
            citizen['birth_date'] = date
            validate_date(date)
            citizen['import_id'] = max_import_id
            relatives.append(
                {
                    citizen['citizen_id']: citizen.pop('relatives')
                }
            )
            Citizen.objects.create(**citizen)
        except (ValueError, ValidationError, DateError):
            return HttpResponse(status=400)
    for relative in relatives:
        for citizen_id, current_relatives in relative.items():
            instance = Citizen.objects.filter(citizen_id=citizen_id, import_id=max_import_id).first()
            instances_relatives = Citizen.objects.filter(citizen_id__in=current_relatives,
                                                         import_id=max_import_id).all()
            instance.relatives.add(*instances_relatives)

    return JsonResponse({'data': {'import_id': 1}}, status=201)


@csrf_exempt
@require_http_methods('PATCH')
def import_update(request, import_id, citizen_id):
    pass