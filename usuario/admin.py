from django.contrib import admin
from .models import Preferencia

# Register your models here.
class PreferenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'escola')


admin.site.register(Preferencia, PreferenciaAdmin)
