from django.contrib import admin

# Register your models here.
from .models import VehicleService
from .models import ServicePart

from .models import ServiceDocument


admin.site.register(VehicleService)
admin.site.register(ServicePart)
admin.site.register(ServiceDocument)
