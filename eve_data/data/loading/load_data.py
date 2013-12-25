import os.path
import zipfile

from eve_data.data.loading import configs, utils
from eve_data.data import sql

def load_data():
    for table_name, data in configs.loading_data.items():
        filename = table_name + '.sql'
        full_path = os.path.join(sql.__path__[0], filename + '.zip')
        zp = zipfile.ZipFile(full_path)
        contents = zp.read('sql/{0}'.format(filename))
        model_instances = []
        for row in utils.get_fields(contents, data['fields']):
            try:
                model_instances.append(data['model'](**row))
            except ValueError:
                continue
        data['model'].objects.bulk_create(model_instances)
