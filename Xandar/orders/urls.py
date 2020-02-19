from django.urls import path
from .views import show_ordered_items, apply_coupon, place_order, get_delivery_addresses, order_successful_page, \
    GetOrderedItems, add_address, post_review, delete_address, UpdateAddress

app_name='orders'
urlpatterns = [
    path('', show_ordered_items, name='checkout'),
    path('apply/', apply_coupon, name='apply_name'),
    path('place_order/',place_order, name='place_order'),
    path('successful/', order_successful_page, name='order_successful'),
    path('address/',get_delivery_addresses.as_view(), name='delivery_address'),
    path('add_address/', add_address, name='add_address'),
    path('delete_address/<int:pk>/', delete_address, name='delete_address'),
    path('update_address/<int:pk>/', UpdateAddress.as_view(), name='update_address'),
]

urlpatterns += [
    path('your_orders/', GetOrderedItems.as_view(), name='ordered_items'),
    path('post_review/<int:pk>/', post_review, name='post_review'),
]
