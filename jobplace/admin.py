from django.contrib import admin
from .models import PlaceModel,DateModel,TimeModel,CustomUser,RegisterModel
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _ 
from django.utils.html import format_html

class PlaceModelAdmin(ImportExportModelAdmin):
    list_display = ['id','place']

class DateModelAdmin(ImportExportModelAdmin):
    list_display = ['id','date']

class TimeModelAdmin(ImportExportModelAdmin):
    list_display = ['id','time']

class RegisterModelAdmin(ImportExportModelAdmin):
    list_display = ['id','user','place','date','time']

class CustomUserAdmin(UserAdmin,ImportExportModelAdmin):
    list_display = ['id','username','address']

admin.site.register(PlaceModel,PlaceModelAdmin)
admin.site.register(DateModel,DateModelAdmin)
admin.site.register(TimeModel,TimeModelAdmin)
admin.site.register(RegisterModel,RegisterModelAdmin)
admin.site.register(CustomUser,CustomUserAdmin)