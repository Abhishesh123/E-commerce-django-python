from Xandar import settings
from core.models import Cart, ProductCategory, Product, Attribute, ProductSubcategory


def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
            return {'count': len(cart.cartitems_set.all())}
        except Cart.DoesNotExist:
            return {'count': 0}
    else:
        request.session[settings.CART_SESSION_ID] = request.session.get(settings.CART_SESSION_ID, {})
        if request.session[settings.CART_SESSION_ID] is None:
            return {'count': 0}
        return {'count': len(request.session[settings.CART_SESSION_ID])}

def categories(request):
    return {'category': ProductCategory.objects.order_by().distinct()}

def sub_category(request):
    category = request.session.get("category", None)
    sub_categories = None
    sub_categories_all = None
    if category:

        if category == "All":
            sub_categories_all = ProductCategory.objects.order_by().distinct()

        else:
            sub_category = set()
            try:
                category = ProductCategory.objects.get(category=category)
                sub_categories = sub_category.union(set([item.sub_category for item in Product.objects.filter(category=category)]))

            except ProductCategory.DoesNotExist:
                sub_categories_all = ProductCategory.objects.order_by().distinct()
    return {"sub_category": sub_categories, "sub_category_all": sub_categories_all}

def price(request):
    return {'product_count': Product.objects.all().count()}

def brand(request):
    return {'brands': Attribute.objects.order_by().distinct().values('value')}

def filter_attributes(request):
    sub_category = request.session.get("sub_category", None)
    category = request.session.get("category", None)
    attributes = None
    colors = None

    if sub_category:
        attribute = set()
        color = set()

        try:
            # category = ProductCategory.objects.get(category=category)
            sub_category = ProductSubcategory.objects.get(sub_category=sub_category)
            products = Product.objects.filter(sub_category=sub_category)
            for product in products:
                attribute = attribute.union(set([item.value for item in product.attribute_set.all()]))
                color = color.union(set([item.color for item in product.color_set.all()]))

        except ProductCategory.DoesNotExist:
            pass
        except ProductSubcategory.DoesNotExist:
            pass

        colors = color
        attributes = attribute

    return {"attributes": attributes, "colors": colors }
    