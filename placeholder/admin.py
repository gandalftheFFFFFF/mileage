from django.contrib import admin
from .models import MilageInstance

# Register your models here.
class MilageAdmin(admin.ModelAdmin):
    pass

admin.site.register(MilageInstance, MilageAdmin)