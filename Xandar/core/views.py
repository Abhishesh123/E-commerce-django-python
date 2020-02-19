from django.shortcuts import render, redirect
from .models import Product, ProductImage, Banner, TopBanner, Newsletter
from django.views.generic.list import ListView
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse


class Index(ListView):
    model = Product
    template_name = "core/index.html"
    queryset = Product.objects.filter().order_by('-id')[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['image']=[]
        context['banners'] = Banner.objects.filter(is_active=True)
        context['latest_products'] = Product.objects.order_by("-id")[:9]
        context['top_banners'] = TopBanner.objects.filter(is_active=True)
        context['trending'] = Product.objects.order_by("-count")[:4]

        # Add in a QuerySet of all the books
        # for object in context['object_list']:
        # object.image = Product.objects.filter(name=object.name).main_image
        # print(context['image'])
        for object in context['object_list']:
            # print(object.main_image)
            print(object)
            object.image = ProductImage.objects.filter(product=object).first().image

        for object in context['latest_products']:
            object.image = ProductImage.objects.filter(product=object).first().image

        for object in context['trending']:
            object.image = ProductImage.objects.filter(product=object).first().image

        return context

def news_letter(request):
    if request.method == 'POST':
        email = request.POST['email']
        if not Newsletter.objects.filter(email=email).exists():
            user = Newsletter.objects.create(email=email)

            html_content = render_to_string('core/newsletter.html')

            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives('Subscription to Newsletter', text_content,
                                         'contact.realestate.information@gmail.com', [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponse('Successfully Registered')
        else:
            return HttpResponse('Email Already Exists')

def unsubscribe(request):
    if request.user.is_authenticated:
        try:
            news = Newsletter.objects.filter(email=request.user, is_active=True)
            news.is_active = False
            news.save()
        except Newsletter.DoesNotExist:
            return redirect('accounts:login_app')

    return render(request, 'core/unsubscribe.html')