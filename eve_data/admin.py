from django.contrib import admin

from eve_data import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'group']
    list_display_links = ['name']
    search_fields = ['name', 'id', 'group__name']


class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name', 'id', 'category__name']


class StationAdmin(admin.ModelAdmin):
    def station_sec(self, obj):
        return obj.solar_system.get_display_sec()

    list_display = ['solar_system', 'constellation', 'region', 'station_sec']
    search_fields = [
        'name',
        'id',
        'solar_system__name',
        'constellation__name',
        'region__name'
    ]


class SolarSystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'constellation', 'region', 'get_display_sec']
    list_filter = ['region']
    search_fields = ['name', 'id', 'constellation__name', 'region__name']


class ConstellationAdmin(admin.ModelAdmin):
    list_display = ['name', 'region']
    list_filter = ['region']
    search_fields = ['name', 'id', 'region__name']


admin.site.register(models.ItemCategory)
admin.site.register(models.ItemMaterials)
admin.site.register(models.Region)

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
admin.site.register(models.Constellation, ConstellationAdmin)
admin.site.register(models.SolarSystem, SolarSystemAdmin)
admin.site.register(models.Station, StationAdmin)