# Register your models here.
from django.contrib import admin
from iotshm_dashboard.models import Building

class BuildingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name','number', 'manager']}),
        ('Location',         {'fields': ['address', 'city', 'state', 'zipcode']}),
    ]
    list_display = ('name','number', 'manager','address', 'city', 'state', 'zipcode')
    list_filter = ['number','manager', 'name']
    search_fields = ['number','manager']

admin.site.register(Building,BuildingAdmin)