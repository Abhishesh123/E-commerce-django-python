from django.urls import path

from . import views

app_name = 'operations'

urlpatterns = [
    path('wishlist/add/<int:pk>/', views.add_wishlist_item, name='add_wishlist_items'),
    path('wishlist/', views.list_wishlist_items, name='wishlist'),
    path('wishlist/add_to_cart/<int:product_id>/', views.add_wishlist_to_cart, name='wishlist_to_cart'),
    path('delete-item/<int:pk>/', views.delete_wishlist_items, name='delete_wishlist_items'),
    path('orders/', views.show_orders, name='orders'),
    # path('address/', views.show_address, name='address'),
    path('track/', views.track_order, name='track'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_cart'),
    path('cart/', views.get_cart, name='view_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/delete/<int:product_id>/', views.delete_cart, name='delete_cart'),
]

urlpatterns+=[
path('update/', views.update_cart, name='add_wishlist_items'),
]
