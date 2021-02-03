from django.urls import path

from .views import import_create, import_update

urlpatterns = [
    path('imports', import_create, name='citizen_create'),
    path('imports/<int:import_id>/citizens/<int:citizen_id>', import_update, name='citizen_update'),
    #path('imports/<int:inpoer_id>/citizens'),
]