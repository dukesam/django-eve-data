from neo4jrestclient import client

from django.conf import settings
from django.db import models


class ItemCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Item categories'
        ordering = ['name']


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

    def __unicode__(self):
        return '{material} amount in {item}'.format(
            material=self.material.name, item=self.item.name)

    class Meta:
        unique_together = ('item', 'material')
        verbose_name_plural = 'Item materials'


class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    radius = models.DecimalField(max_digits=20, decimal_places=0)
    x = models.DecimalField(max_digits=20, decimal_places=0)
    y = models.DecimalField(max_digits=20, decimal_places=0)
    z = models.DecimalField(max_digits=20, decimal_places=0)
    min_x = models.DecimalField(max_digits=20, decimal_places=0)
    min_y = models.DecimalField(max_digits=20, decimal_places=0)
    min_z = models.DecimalField(max_digits=20, decimal_places=0)
    max_x = models.DecimalField(max_digits=20, decimal_places=0)
    max_y = models.DecimalField(max_digits=20, decimal_places=0)
    max_z = models.DecimalField(max_digits=20, decimal_places=0)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class Region(Location):
    pass


class Constellation(Location):
    region = models.ForeignKey(Region)


class SolarSystem(Location):
    region = models.ForeignKey(Region)
    constellation = models.ForeignKey(Constellation)
    border = models.BooleanField(default=False)
    dead_end = models.BooleanField(default=False)
    corridor = models.BooleanField(default=False)
    hub = models.BooleanField(default=False)
    inter_regional = models.BooleanField(default=False)
    inter_constellational = models.BooleanField(default=False)
    security = models.DecimalField(max_digits=6, decimal_places=5)
    connections = models.ManyToManyField(
        'self',
        blank=True,
        null=True,
        symmetrical=True,
    )

    def get_nodes_within(self, jump_range=5, security=0.45):
        gdb = client.GraphDatabase(settings.EVE_DATA_NEO4J_INSTANCE)

        dst_ids = [s[0] for s in gdb.query(
            """
                match p=(src {name: {system_id}})-[r:Connects*1..%d]->(dst)
                where all(n in nodes(p) where n.security > {security})
                return dst.name
            """ % (jump_range),
            {'system_id': self.id , 'security': security}
        )]

        return SolarSystem.objects.filter(id__in=dst_ids)

    def get_display_sec(self):
        return round(self.security, 1)


class Station(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    solar_system = models.ForeignKey(SolarSystem, related_name='stations')
    constellation = models.ForeignKey(Constellation, related_name='stations')
    region = models.ForeignKey(Region, related_name='stations')
    security = models.DecimalField(max_digits=6, decimal_places=5)
    reprocessing_efficiency = models.DecimalField(max_digits=3, decimal_places=2)
    reprocessing_cost = models.DecimalField(max_digits=3, decimal_places=2)

    def __unicode__(self):
        return self.name