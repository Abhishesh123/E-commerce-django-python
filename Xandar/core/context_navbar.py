from .models import Product, ProductCategory, ProductSubcategory

def navbar_context(request):
	my_context = {
		'product_categories' : ProductCategory.objects.filter(is_active=True),
		'product_subcategories' : ProductSubcategory.objects.filter(is_active=True),
		'featured_products' : Product.objects.filter(is_featured=True)
	}

	return my_context
	