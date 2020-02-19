"""Xandar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Xandar import settings
from django.contrib.auth import views as auth_views
from accounts import views
from products.views import ProductListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('', include('core.urls')),
    path('product/', include('products.urls')),
    path('operations/', include('operations.urls')),
    path('product_list/', ProductListView.as_view(), name="product_list"),
    path('orders/', include('orders.urls')),



    

























    path('forgot_password/', views.check_email, name="check_email"),


    path('password-reset', 
    	auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html', html_email_template_name="accounts/email_reset_template.html",
            email_template_name='accounts/password_reset_email.html', subject_template_name="accounts/password_reset_subject.txt",
            ),
    		 name="password_reset"),

    path('password-reset/done', 
    	auth_views.PasswordResetDoneView.as_view(
    		template_name='accounts/password_reset_done.html'),
    		 name="password_reset_done"),

    path('password-reset-complete/', 
    	auth_views.PasswordResetCompleteView.as_view(
    		template_name='accounts/password_reset_complete.html'),
    		 name="password_reset_complete"),

    path('password-reset-confirm/<uidb64>/<token>/', 
    	auth_views.PasswordResetConfirmView.as_view(
    		template_name='accounts/password_reset_confirm.html'),
    		 name="password_reset_confirm"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
