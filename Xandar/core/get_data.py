from .models import *


def get_dataset(*args, **kwargs):
    table = args[0]
    dataset = table.objects.filter(**kwargs)
    return dataset


def get_data(*args, **kwargs):
    table = args[0]
    try:
        data = table.objects.get(**kwargs)
        return data
    except table.DoesNotExist:
        return None


def create_data(*args, **kwargs):
    table = args[0]
    table.objects.create(**kwargs)