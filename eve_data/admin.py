from django.contrib import admin

from eve_data import models

admin.site.register(models.Item)
admin.site.register(models.ItemGroup)
admin.site.register(models.ItemCategory)