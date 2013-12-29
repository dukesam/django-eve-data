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


class SolarSystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'constellation', 'region', 'security']
    list_filter = ['region']
    search_fields = ['name', 'id', 'constellation__name', 'region__name']



admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
admin.site.register(models.ItemCategory)
admin.site.register(models.ItemMaterials)
admin.site.register(models.Region)
admin.site.register(models.Constellation)
admin.site.register(models.SolarSystem, SolarSystemAdmin)
admin.site.register(models.Station)