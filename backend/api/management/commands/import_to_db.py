import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Import ingredients to DB from json'

    def add_arguments(self, parser):
        parser.add_argument(
            'ingredients',
            default='ingredients.json',
            nargs='?',
            type=str)
        parser.add_argument(
            'tags',
            default='tags.json',
            nargs='?',
            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(
                settings.MEDIA_ROOT + '/data/', options['tags']), 'r',
                    encoding='utf-8') as f:
                data_tags = json.load(f)
                for tag in data_tags:
                    try:
                        Tag.objects.create(name=tag['name'],
                                           color=tag['color'],
                                           slug=tag['slug'])
                    except IntegrityError:
                        print(f'В базе уже есть: {tag["name"]} ')

            with open(os.path.join(
                settings.MEDIA_ROOT + '/data/', options['ingredients']), 'r',
                    encoding='utf-8') as f:
                data = json.load(f)
                for ingredient in data:
                    try:
                        Ingredient.objects.create(name=ingredient['name'],
                                                  measurement_unit=ingredient[
                                                      'measurement_unit'])
                    except IntegrityError:
                        print(f'В базе уже есть: {ingredient["name"]} '
                              f'({ingredient["measurement_unit"]})')

        except FileNotFoundError:
            raise CommandError('Файл отсутствует в директории media/data')
