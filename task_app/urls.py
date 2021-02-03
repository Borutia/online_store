from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import CreateImports

urlpatterns = [
    path('imports', CreateImports.as_view(), name='citizen_create'),
]