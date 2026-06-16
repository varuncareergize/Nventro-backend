from django.contrib import admin
from .models import Part, PartUsage, PartTransaction

admin.site.register(Part)
admin.site.register(PartUsage)
admin.site.register(PartTransaction)
