from django.urls import path

from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.index, name='home'),
    path('categorie/<slug:slug>/', views.category_detail, name='category_detail'),
    path('article/<slug:slug>/', views.post_detail, name='post_detail'),
]
