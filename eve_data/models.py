from django.db import models

class ItemCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class ItemGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(ItemCategory, related_name='groups', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    base_price = models.BooleanField(default=False)
    allow_manufacture = models.BooleanField(default=False)
    allow_recycle = models.BooleanField(default=False)
    anchored = models.BooleanField(default=False)
    allow_anchor = models.BooleanField(default=False)
    fittable_non_singleton = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(ItemGroup, related_name='items', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mass = models.DecimalField(max_digits=50, decimal_places=0, default=0)
    volume = models.DecimalField(max_digits=50, decimal_places=2)
    capacity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    portion_size = models.IntegerField(blank=True, null=True)
    race = models.CharField(max_length=255, blank=True, null=True)
    published = models.BooleanField(default=False)
    market_group_id = models.IntegerField(blank=True, null=True)

    materials = models.ManyToManyField(
        'self',
        through='ItemMaterials',
        symmetrical=False,
        related_name='materials+'
    )

    def __unicode__(self):
        return self.name

class ItemMaterials(models.Model):
    item = models.ForeignKey(Item, related_name='components')
    material = models.ForeignKey(Item, related_name='assembled_with')
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('item', 'material')