from collections import namedtuple
from decimal import Decimal
import random
import re


STR_RE = re.compile("[']([^']+)[']")
FieldData = namedtuple('FieldData', ['name', 'pos', 'convert'])


def to_int(value):
    return int(value)


def to_dec(value):
    return Decimal(value)


def to_bool(value):
    return bool(int(value))


def to_str(value):
    return value


def to_model(model):
    def func(value):
        try:
            return model.objects.get(id=value)
        except model.DoesNotExist:
            return None
    return func


class StringHider(object):
    base_key = 'GROUP-{0}'

    def __init__(self):
        self.storage = {}

    def hide(self, matchobj):
        while True:
            key = self.base_key.format(random.randint(0, 1000))
            if key not in self.storage:
                break
        self.storage[key] = matchobj.group(1)
        return key


def get_fields(path, field_handling):
    fo = open(path, 'r')
    for line in fo.readlines():
        if not line.startswith('INSERT'):
            continue

        line = re.sub(r'\\r\\n', r'\n', line)
        line = re.sub(r"\\'", '"', line)

        for item in re.findall('[(]([^)]+)[)](?=[,][(])', line):
            hider = StringHider()
            item = re.sub(STR_RE, hider.hide, item)

            pieces = item.split(',')
            for i, p in enumerate(pieces):
                if p == 'NULL':
                    pieces[i] = None
                elif p in hider.storage:
                    pieces[i] = hider.storage[p]
            kwargs = {}
            for field_def in field_handling:
                kwargs[field_def.name] = field_def.convert(pieces[field_def.pos])

            yield kwargs