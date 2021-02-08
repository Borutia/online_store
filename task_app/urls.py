from django.urls import path, re_path

from .views import Imports, CitizenBirthdays, CitizenPercentileAge

urlpatterns = [
    path('imports', Imports.as_view(), name='citizen_create'),
    path('imports/<int:import_id>/citizens/<int:citizen_id>', Imports.as_view(), name='citizen_update'),
    path('imports/<int:import_id>/citizens', Imports.as_view(), name='citizens_get'),
    path('imports/<int:import_id>/citizens/birthdays', CitizenBirthdays.as_view(), name='citizen_birthdays'),
    path('imports/<int:import_id>/towns/stat/percentile/age', CitizenPercentileAge.as_view(), name='citizen_percentile_age'),
]