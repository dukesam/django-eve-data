from django.core.management.base import BaseCommand, CommandError

from eve_data import models
from eve_data.data.loading import load_data

class Command(BaseCommand):
    args = ''
    help = 'Load data.'

    def handle(self, *args, **options):
        models.Item.objects.all().delete()
        models.ItemGroup.objects.all().delete()
        models.ItemCategory.objects.all().delete()

        load_data.load_data()

        self.stdout.write('Loaded!')
