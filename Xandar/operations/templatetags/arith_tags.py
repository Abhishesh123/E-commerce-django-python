from django import template

from core.models import Product, ProductCategory

register = template.Library()


@register.simple_tag
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price

@register.simple_tag
def count_category(category):
    try:
        count_cat = Product.objects.filter(category=category).count()
        return count_cat
    except ProductCategory.DoesNotExist:
        return 0

@register.simple_tag
def count_sub_category(sub_category):
    try:
        count_cat = sub_category.product_set.all().count()
        return count_cat
    except Product.DoesNotExist:
        return 0

@register.filter
def count_objs(objects):
    if objects:
        return len(objects)
    return 0

# @register.tag
# def trim(name):
#     return name.split(" ")[0]
