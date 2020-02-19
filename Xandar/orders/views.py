from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response

from core.get_data import get_data
from core.models import OrderedItems, DeliveryAddresses, Customer, Wishlist, Cart, CartItems, ProductImage, Product, \
    Review
from django.views.generic import ListView, UpdateView

from orders.forms import UpdateAddress
from products.views import ProductDetailView
from datetime import datetime
from core.models import Coupons
# Create your views here.


def show_ordered_items(request):
    context = {}

    if request.method == 'POST':
        pass
    else:
        if request.user.is_authenticated:
            try:
                current_cart = Cart.objects.get(user_id=request.user.id)
                orders = CartItems.objects.filter(cart_id=current_cart)
                delivery_addresses = DeliveryAddresses.objects.filter(customer=request.user)
                context = {
                    'orders':orders,
                    'addresses': delivery_addresses
                }
            except Cart.DoesNotExist:
                context = {
                    'orders': False
                }
            return render(request, 'orders/checkout.html', context)
        else:
            return redirect('accounts:login_app')



def apply_coupon(request):
    coupon = request.GET['coupon']
    total = int(request.GET['total'])
    if coupon == 'FIRST':
        discount = 0.10 * total
    else:
        discount  = 0
    total = total-discount
    return HttpResponse(total)


def place_order(request):
    address_dict={}
    for key, values in request.GET.items():
        address_dict[key] = values
    UserAddress = DeliveryAddresses()
    for key, values in request.GET.items():
            setattr(UserAddress, key, request.GET[key])
    UserAddress.customer = request.user
    address_exists = get_data(DeliveryAddresses,
             receiver_name=UserAddress.receiver_name,
             customer=UserAddress.customer,
             phone_number=UserAddress.phone_number,
             city=UserAddress.city,
             pincode=UserAddress.pincode,
             state=UserAddress.state
             )
    if address_exists is None:
        UserAddress.save()
    request.session['order_context'] = request.GET
    return HttpResponse('Order Placed Successful')


class get_delivery_addresses(ListView):
    template_name = 'orders/delivery_address.html'
    context_object_name = "address"

    def get_queryset(self):
        queryset = DeliveryAddresses.objects.filter(customer=self.request.user)
        return queryset

    def post(self,id):
        pass


def order_successful_page(request):
    context = request.session.get('order_context')
    current_cart = Cart.objects.get(user_id=request.user.id)
    orders = CartItems.objects.filter(cart_id=current_cart)
    for order in orders:
        OrderedItems.objects.create(customer=request.user,
                                    title=order.product.name,
                                    slug=order.product.slug,
                                    image=order.product_img.image,
                                    description=order.product.description,
                                    price=order.product.price,
                                    quantity=order.quantity)
    context['orders'] = orders
    current_cart.delete()
    return render(request, 'orders/order_confirmed.html', context)


class GetOrderedItems(ListView):
    template_name = 'orders/ordered_items.html'
    
    def get_queryset(self):
        queryset = OrderedItems.objects.filter(customer=self.request.user).order_by('-order_date')
        return queryset


def add_address(request):

    if request.user.is_authenticated:

        if request.method == "POST":
            name = request.POST['name']
            phone = request.POST['phone']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            city = request.POST['city']
            pin = request.POST['pin']
            state = request.POST.get('state')

            user = DeliveryAddresses.objects.create(customer=request.user, receiver_name=name, street_address=address1,
                                                    city=city, phone_number=phone, pincode=pin, state=state)

            return redirect('orders:delivery_address')

    return render(request, 'orders/add_address.html',)


def post_review(request, pk):
    product = Product.objects.get(pk=pk)
    customer = request.user
    message = request.POST.get('message')
    customer_full_name = customer.first_name + " " + customer.last_name
    Review.objects.create(customer_name=customer_full_name, product=product, message=message)
    return HttpResponse('Response Posted Successfully')


def apply_coupon(request):
    coupon_name = request.GET.get('coupon', None)

    if coupon_name:
        try:
            coupon = Coupons.objects.get(name=coupon_name)
            valid_till = coupon.valid_till

            remainder = int(datetime.now().day - valid_till.day)

            if remainder > 0:
                return HttpResponse("Coupon Expired")

            discount_percentage = coupon.discount % 100
            total = int(request.GET['total'])

            total = total - discount_percentage
            return HttpResponse(total)

        except Coupons.DoesNotExist:
            return HttpResponse("Invalid Coupon No Discount")
    else:
        return HttpResponse("Provide a valid Coupon Name")

@login_required
def delete_address(request, pk):
    DeliveryAddresses.objects.get(id=pk).delete()
    return redirect('orders:delivery_address')

class UpdateAddress(LoginRequiredMixin, UpdateView):
    model = DeliveryAddresses
    template_name = 'orders/update_address.html'
    context_object_name = 'details'
    form_class = UpdateAddress

    def form_valid(self, form):
        form.save()
        return redirect('orders:delivery_address')




