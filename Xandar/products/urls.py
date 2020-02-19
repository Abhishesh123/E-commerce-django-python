from django.urls import path, include, re_path
from . import views
app_name = 'products'
urlpatterns = [
    re_path(r'^category=(?P<category>\w+)(&&sub=(?P<sub>[\w-]+)|&&price_lte=(?P<price_lte>\d+)|&&price_gte=(?P<price_gte>\d+)|&&brand=(?P<brand>[\w\s.]+)|&&color=(?P<color>\w+)|&&text=(?P<text>[A-Za-z0-9\s]+))*', views.filter_by, name="product_filter"),
    #re_path(r'^category=(?P<category>\w+)|price=(?P<price>\d+)', views.filter_by),
    #re_path(r'^brand=(?P<brand>\w+)', views.filter_by),
    path('<slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/<int:pk>', views.product_add_wishlist_cart, name='product_add'),
    path('search_result/', views.search_result, name="search_result")

]


"""
from django.urls import path, include, re_path
from . import views
app_name = 'products'
urlpatterns = [
    re_path(r'^(category=(?P<category>\w+)&&price=(?P<price>\d+))', views.filter_by),
    re_path(r'^category=(?P<category>\w+)|price=(?P<price>\d+)', views.filter_by),
    path('<slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/<int:pk>', views.product_add_wishlist_cart, name='product_add'),

]

"""