from django.contrib import admin
from measurementapp import models as measurementapp_models

# Register your models here.
class MeasurementAdmin(admin.ModelAdmin):
    pass


admin.site.register(measurementapp_models.Measurement, MeasurementAdmin)
