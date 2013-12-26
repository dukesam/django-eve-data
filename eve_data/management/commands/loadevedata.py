from django.core.management.base import BaseCommand, CommandError

from eve_data.data.loading import load_data

class Command(BaseCommand):
    args = ''
    help = 'Process all SQL files and load the data into models.'

    def handle(self, *args, **options):
        load_data.load_data()

        self.stdout.write('Loaded!')
