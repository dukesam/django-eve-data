import os.path

from eve_data.data.loading import configs, utils
from eve_data.data import sql

def load_data():
    for table_name, data in configs.loading_data.items():
        full_path = os.path.join(sql.__path__[0], table_name + '.sql')
        for row in utils.get_fields(full_path, data['fields']):
            data['model'].objects.create(**row)
