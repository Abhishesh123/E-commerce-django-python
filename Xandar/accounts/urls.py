from django.urls import path, re_path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_page, name='login_app'),
    path('logout/', views.logout_user, name='logout_app'),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('register/', views.user_register, name='registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    re_path('[A-Za-z0-9]*', views.login_page, name='login_app'),

]
