from django.urls import path
from core import views
urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('newsletter/', views.news_letter, name='newsletter'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]