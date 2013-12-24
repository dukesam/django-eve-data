from collections import OrderedDict

from eve_data import models
from eve_data.data import sql
from eve_data.data.loading import utils
from eve_data.data.loading.utils import FieldData

loading_data = OrderedDict((
    (
        'invCategories',
        {
            'fields': [FieldData(*x) for x in [
                ('id', 0, utils.to_int),
                ('name', 1, utils.to_str),
                ('description', 2, utils.to_str),
            ]],
            'model': models.ItemCategory,
        },
    ),
    (
        'invGroups',
        {
            'fields': [FieldData(*x) for x in [
                ('id', 0, utils.to_int),
                ('category', 1, utils.to_model(models.ItemCategory)),
                ('name', 2, utils.to_str),
                ('description', 3, utils.to_str),
                ('base_price', 5, utils.to_int),
                ('allow_manufacture', 6, utils.to_bool),
                ('allow_recycle', 7, utils.to_bool),
                ('anchored', 8, utils.to_bool),
                ('allow_anchor', 9, utils.to_bool),
                ('fittable_non_singleton', 10, utils.to_bool),
            ]],
            'model': models.ItemGroup,
        },
    ),
    (
        'invTypes',
        {
            'fields': [FieldData(*x) for x in [
                ('id', 0, utils.to_int),
                ('group', 1, utils.to_model(models.ItemGroup)),
                ('name', 2, utils.to_str),
                ('description', 3, utils.to_str),
                ('mass', 4, utils.to_dec),
                ('volume', 5, utils.to_dec),
                ('capacity', 6, utils.to_dec),
                ('portion_size', 7, utils.to_int),
                ('race', 8, utils.to_str),
                ('published', 10, utils.to_bool),
                ('market_group_id', 11, utils.to_str),
            ]],
            'model': models.Item,
        },
    ),
    (
        'invTypeMaterials',
        {
            'fields': [FieldData(*x) for x in [
                ('item', 0, utils.to_model(models.Item)),
                ('material', 1, utils.to_model(models.Item)),
                ('quantity', 2, utils.to_int),
            ]],
            'model': models.ItemMaterials,
        }

    ),
    (
        'mapRegions',
        {
            'fields': [FieldData(*x) for x in [
                ('id', 0, utils.to_int),
                ('name', 1, utils.to_str),
                ('x', 2, utils.to_dec),
                ('y', 3, utils.to_dec),
                ('z', 4, utils.to_dec),
                ('min_x', 5, utils.to_dec),
                ('max_x', 6, utils.to_dec),
                ('min_y', 7, utils.to_dec),
                ('max_y', 8, utils.to_dec),
                ('min_z', 9, utils.to_dec),
                ('max_z', 10, utils.to_dec),
                ('radius', 12, utils.to_dec),
            ]],
            'model': models.Region,
        }
    ),
))