import csv
from datetime import datetime
from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Genre,
    GenreTitle,
    Title,
    User,
    Review,
    Comment
)


dict_model = {
    'category': Category,
    'genre': Genre,
    'title': Title,
    'genretitle': GenreTitle,
    'users': User,
    'review': Review,
    'comment': Comment
}


class Command(BaseCommand):
    help = 'Create model objects'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="file path")
        parser.add_argument('--model_name', type=str, help="model name")

    def __get_dict_object(self, object_dict):
        new_dict = {}
        for key, value in object_dict.items():
            if key == 'author':
                value = User.objects.get(pk=value)
            elif key == 'pub_date':
                date = datetime.fromisoformat(
                    str(value).split('.')[0],
                )
                value = date
            else:
                for name_model in dict_model.keys():
                    if key.startswith(name_model):
                        id_model = dict_model[name_model]
                        value = id_model.objects.get(pk=value)
                        key = name_model
            new_dict[key] = value
        return new_dict

    def handle(self, *args, **options):
        file_path = options['path']
        try:
            model = dict_model[options['model_name']]
            if file_path and model:
                with open(file_path) as csv_file:
                    for row in csv.DictReader(csv_file):
                        data = self.__get_dict_object(row)
                        model.objects.create(**data)
        except Exception:
            print('Не существующая модель')
