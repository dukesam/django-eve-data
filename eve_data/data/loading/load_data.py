import os.path
import zipfile

from django.conf import settings

from eve_data import models
from eve_data.data.loading import configs, utils
from eve_data.data import sql


def get_table_contents(table_name):
    filename = table_name + '.sql'
    full_path = os.path.join(sql.__path__[0], filename + '.zip')
    zp = zipfile.ZipFile(full_path)
    return zp.read('sql/{0}'.format(filename))


def load_data():
    for table_name, data in configs.loading_data.items():
        data['model'].objects.all().delete()
        contents = get_table_contents(table_name)
        model_instances = []
        for row in utils.get_fields(contents, data['fields']):
            try:
                model_instances.append(data['model'](**row))
            except ValueError:
                continue
        data['model'].objects.bulk_create(model_instances)

    connections = {}
    conn_contents = get_table_contents('mapSolarSystemJumps')
    for row in utils.get_raw_fields(conn_contents):
        src, dst = int(row[2]), int(row[3])
        if src not in connections:
            connections[src] = []
        connections[src].append(dst)

    systems = {system.id: system for system in models.SolarSystem.objects.all()}
    for sys_id, system in systems.items():
        dst_systems = [systems[s] for s in connections.get(sys_id, [])]
        system.connections.add(*dst_systems)

    if hasattr(settings, 'EVE_DATA_NEO4J_INSTANCE'):
        from neo4jrestclient.client import GraphDatabase
        gdb = GraphDatabase(settings.EVE_DATA_NEO4J_INSTANCE)

        nodes = {sys_id: gdb.nodes.create(name=sys_id) for sys_id in systems}
        for sys_id, connection_list in connections.items():
            src_node = nodes[sys_id]
            for dst_id in connection_list:
                src_node.relationships.create('Connects', nodes[dst_id])
