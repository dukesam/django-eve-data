from collections import OrderedDict

from eve_data import models
from eve_data.data import sql
from eve_data.data.loading import utils
from eve_data.data.loading.utils import FieldData

loading_data = OrderedDict((
    (
        'invCategories',
        {
            'fields': [
                FieldData('id', 0, utils.to_int),
                FieldData('name', 1, utils.to_str),
                FieldData('description', 2, utils.to_str),
            ],
            'model': models.ItemCategory,
        },
    ),
    (
        'invGroups',
        {
            'fields': [
                FieldData('id', 0, utils.to_int),
                FieldData('category', 1, utils.to_model(models.ItemCategory)),
                FieldData('name', 2, utils.to_str),
                FieldData('description', 3, utils.to_str),
            ],
            'model': models.ItemGroup,
        },
    ),
    (
        'invTypes',
        {
            'fields': [
                FieldData('id', 0, utils.to_int),
                FieldData('group', 1, utils.to_model(models.ItemGroup)),
                FieldData('name', 2, utils.to_str),
                FieldData('description', 3, utils.to_str),
                FieldData('mass', 4, utils.to_dec),
                FieldData('volume', 5, utils.to_dec),
                FieldData('capacity', 6, utils.to_dec),
                FieldData('portion_size', 7, utils.to_int),
                FieldData('race', 8, utils.to_str),
                FieldData('published', 10, utils.to_bool),
                FieldData('market_group_id', 11, utils.to_str),
            ],
            'model': models.Item,
        },
    )
))