from django.contrib import admin
from accountapp import models as accountapp_models

# Register your models here.
class MeasurementAdmin(admin.ModelAdmin):
    pass


admin.site.register(accountapp_models.User, MeasurementAdmin)