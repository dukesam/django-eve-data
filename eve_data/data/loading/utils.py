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
    cache = {}
    def func(value):
        if value not in cache:
            try:
                cache[value] = model.objects.get(id=value)
            except model.DoesNotExist:
                cache[value] = None
        return cache[value]
    return func


class StringHider(object):
    base_key = 'GROUP-{0}'

    def __init__(self):
        self.storage = {}
        self.curr_count = 0

    def hide(self, matchobj):
        self.curr_count += 1
        key = self.base_key.format(self.curr_count)
        self.storage[key] = matchobj.group(1)
        return key


def get_raw_fields(contents):
    for line in contents.splitlines():
        if not line.startswith('INSERT'):
            continue

        line = re.sub(r'\\r\\n', r'\n', line)
        line = re.sub(r"\\'", '"', line)

        for item in re.findall('[(]([^)]+)[)](?=(?:[,][(])|(?:[;]$))', line):
            hider = StringHider()
            item = re.sub(STR_RE, hider.hide, item)

            pieces = item.split(',')
            for i, p in enumerate(pieces):
                if p == 'NULL':
                    pieces[i] = None
                elif p in hider.storage:
                    pieces[i] = hider.storage[p]
            if pieces[2] == 30003459:
                print pieces

            yield pieces


def get_fields(contents, field_handling):
    for pieces in get_raw_fields(contents):
        kwargs = {}
        for field_def in field_handling:
            kwargs[field_def.name] = field_def.convert(pieces[field_def.pos])

        yield kwargs