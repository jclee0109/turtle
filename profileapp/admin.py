from django.contrib import admin
from profileapp import models as profileapp_models

# Register your models here.
class MeasurementAdmin(admin.ModelAdmin):
    pass


admin.site.register(profileapp_models.Profile, MeasurementAdmin)
