import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from Xandar import settings
from core.models import Product, ProductImage, Cart, CartItems, WishlistItems
from core.models import Customer, Wishlist
# Create your views here.
from operations.forms import UpdateCartForm


@login_required
def list_wishlist_items(request):
    error = ''
    try:
        wishlist = Wishlist.objects.get(customer=request.user)
        items = WishlistItems.objects.filter(wishlist=wishlist)
        imagelist = [item.product.productimage_set.all()[0].image for item in items]
        items = zip(items, imagelist)

    except Wishlist.DoesNotExist:
        items = []
        error = "Your wishlist is empty"
    if len(imagelist) == 0:
        error = "Your wishlist is empty"

    return render(request, 'operations/wishlist.html', {"items": items, 'error': error})

@login_required
def add_wishlist_item(request, pk):
    # if request.user.is_authenticated:
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return HttpResponse('The Product you are trying to add does not exist')

    try:
        wishlist = Wishlist.objects.get(customer=request.user)
    except Wishlist.DoesNotExist:
        Wishlist.objects.create(customer=request.user)

    wishlist = Wishlist.objects.get(customer=request.user)

    try:
        WishlistItems.objects.get(wishlist=wishlist, product=product)
        return HttpResponse("Item already in wishlist")
    except WishlistItems.DoesNotExist:
        WishlistItems.objects.create(wishlist=wishlist, product=product)
        return HttpResponse("Item Added To Wishlist Successfully")

@login_required
def add_wishlist_to_cart(request, product_id):
    add_to_cart(request, product_id)
    delete_wishlist_items(request, product_id)
    return HttpResponse(list_wishlist_items(request))

@login_required
def delete_wishlist_items(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return HttpResponse("Product Doesnot exist")

    try:
        wishlist = Wishlist.objects.get(customer=request.user)
    except Wishlist.DoesNotExist:
        return HttpResponse("Your Wishlist is empty")

    try:
        WishlistItems.objects.get(wishlist=wishlist, product=product).delete()
        return HttpResponse('Item deleted from wishlist Successfully')
    except WishlistItems.DoesNotExist:
        return HttpResponse("No such item exist")

@login_required
def show_orders(request):
    return render(request, 'operations/orders.html')


# def show_address(request):
#     return render(request, 'operations/address.html')


def track_order(request):
    return render(request, 'operations/track.html')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_to_cart(request, product_id, quantity=1):
    errors = ""

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "You are trying to add product that does not exist")
        return render(
            request, 'operations/cart.html')

    product_image = product.productimage_set.all()[0]

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        try:
            obj = CartItems.objects.get(cart=cart, product=product)
            if obj:
                return HttpResponse("You are adding the item that already exist")
        except CartItems.DoesNotExist:

            if quantity <= product.quantity:
                if quantity <= 3:
                    CartItems.objects.create(cart=cart, product=product, product_img=product_image, quantity=quantity,
                                             unit_price=product.price)
                else:
                    return HttpResponse("This item cannot be added more than 3")

            else:
                return HttpResponse(f'Maximum amount available is {product.quantity} !!!!')

    else:

        ip_address = get_client_ip(request)

        request.session[settings.CART_SESSION_ID] = request.session.get(settings.CART_SESSION_ID, {})

        product_id = str(product_id)

        if request.session[settings.CART_SESSION_ID] is None:
            request.session[settings.CART_SESSION_ID] = {}
            request.session[settings.CART_SESSION_ID][product_id] = {
                'product': {'id': product_id, 'name': product.name, 'slug': product.slug},
                'quantity': 0, 'unit_price': product.price,
                'product_img': {'image': {'url': product_image.image.url}}
            }

        elif product_id not in request.session[settings.CART_SESSION_ID]:
            request.session[settings.CART_SESSION_ID][product_id] = {
                'product': {'id': product_id, 'name': product.name, 'slug': product.slug},
                'quantity': 0, 'unit_price': product.price,
                'product_img': {'image': {'url': product_image.image.url}}
            }
        else :
            return HttpResponse("You are adding the item that already exist")

        if quantity <= product.quantity :
            if quantity <= 3:
                request.session[settings.CART_SESSION_ID][product_id]['quantity'] = quantity
                request.session.modified = True
            else:
                return HttpResponse("This item cannot be added more than 3 in cart")
        else:
            return HttpResponse('This item is not available that much you want to avail Sorry !!!!')

    return HttpResponse('Item Added To Cart Successfully')


def get_cart(request):
    errors = ""
    form = UpdateCartForm()

    if request.user.is_authenticated:

        '''Code to add the anonymous cart items to the logged in user'''
        request.session[settings.CART_SESSION_ID] = request.session.get(settings.CART_SESSION_ID, None)
        if request.session[settings.CART_SESSION_ID] is not None:
            try:
                cart = Cart.objects.get(user=request.user, is_ordered=False)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=request.user)

            for item in request.session[settings.CART_SESSION_ID].values():
                product = Product.objects.get(id=int(item['product']['id']))
                product_image = product.productimage_set.all()[0]
                try:
                    items = CartItems.objects.get(cart=cart, product=product)
                except CartItems.DoesNotExist:
                    CartItems.objects.create(cart=cart, product=product,
                                         product_img=product_image, quantity=item['quantity'],
                                         unit_price=product.price)
            del request.session[settings.CART_SESSION_ID]
            request.session.modified = True

        try:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
            print('run')
        except Cart.DoesNotExist:
            messages.error(request, "You don't have anything in cart")
            return render(request, 'operations/cart.html', {'errors': errors})

        items = CartItems.objects.filter(cart=cart)
        if len(items) == 0:
            errors = "You don't have anything in cart"
        total_price = sum(Decimal(item.unit_price) * item.quantity for item in items)

    else:
        items = []
        request.session[settings.CART_SESSION_ID] = request.session.get(settings.CART_SESSION_ID, None)
        if not request.session[settings.CART_SESSION_ID]:
            errors = "You don't have anything in cart"
            return render(
                request, 'operations/cart.html', {'errors': errors})
        count=0
        for item in request.session[settings.CART_SESSION_ID].values():
            count+=1
            # item['price'] = Decimal(item['price'])
            item['total_price'] = item['unit_price'] * item['quantity']
            item['id']=count
            item['product']['price'] = item['unit_price']
            print(item)
            items.append(item)

        total_price = sum(Decimal(item['unit_price']) * item['quantity'] for item in
                          request.session[settings.CART_SESSION_ID].values())
    return render(request, 'operations/cart.html',
                  {'items': items, 'total_price': total_price, 'errors': errors, 'form': form})


def update_cart(request, product_id):
    errors = " "
    global message
    form = UpdateCartForm()
    if request.method == "POST":
        form = UpdateCartForm(request.POST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "You are updating product that does not exist !!!")

        # if form.is_valid():

        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user, is_ordered=False)
            except Cart.DoesNotExist:
                # messages.error(request, "You don't have anything in cart")
                # return render(request, 'operations/cart.html', {'errors': errors})
                message = "You Don't Have Anything In Cart"

            items = CartItems.objects.filter(cart=cart, product=product)[0]
            # quantity = form.cleaned_data['quantity']
            quantity = request.POST.get('qty')
            quantity = int(quantity)

            if quantity <= product.quantity:
                items.quantity = quantity
                items.save()
                message = "Item In Your Cart Updated successfully"
            else:
                message = f"Maximum amount available for {product.name} is {product.quantity} !!"
                #messages.error(request, f"Maximum amount available for {product.name} is {product.quantity} !!")

        else:
            product_id = str(product_id)
            quantity = request.POST.get("qty")
            quantity = int(quantity)

            if quantity <= product.quantity:
                request.session[settings.CART_SESSION_ID][product_id]['quantity'] = quantity
                message = "Item In Your Cart Updated successfully"
                request.session.modified = True
            else:
                message = f"Maximum amount available for {product.name} is {product.quantity} !!"
                #messages.error(request, f"Maximum amount available for {product.name} is {product.quantity} !!")
        # import pdb;
        # pdb.set_trace()
        #html = render(request, 'operations/cart.html')
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
            items = CartItems.objects.filter(cart=cart, product=product)[0]
            output = json.dumps({
                'message': message,
                'item_id': items.id,
                'item_quantity': items.quantity,
            })
        else:
            for item in request.session[settings.CART_SESSION_ID].values():
                if item['product']['id'] == product_id:
                    id = item['id']
            output = json.dumps({
                'message': message,
                'item_id': id,
                'item_quantity': request.session[settings.CART_SESSION_ID][product_id]['quantity'],
            })
        return HttpResponse(output,content_type="application/json")
        #return HttpResponse(output, content_type='application/json')

        return redirect('operations:view_cart')

    return render(request, 'operations/cart.html')


def delete_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "You are updating product that does not exist !!!")

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
        except Cart.DoesNotExist:
            messages.error("You don't have anything in cart")
            return render(request, 'operations/cart.html')

        CartItems.objects.filter(cart=cart, product=product).delete()

    else:
        product_id = str(product_id)
        del request.session[settings.CART_SESSION_ID][product_id]
        request.session.modified = True
    return redirect('operations:view_cart')
