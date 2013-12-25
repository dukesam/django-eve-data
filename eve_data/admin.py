from django.contrib import admin

from eve_data import models

admin.site.register(models.Item)
admin.site.register(models.ItemGroup)
admin.site.register(models.ItemCategory)
admin.site.register(models.ItemMaterials)
admin.site.register(models.Region)
admin.site.register(models.Constellation)
admin.site.register(models.SolarSystem)