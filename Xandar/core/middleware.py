from django.conf import settings
from .models import Cart, CartItems

class CartMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #current_cart = Cart.objects.get(user=request.user)
        #count = CartItems.objects.filter(cart = current_cart).count()
        #request.session['cart_count']=count
        return self.get_response(request)

    def process_exception(self, request, exception):
        pass