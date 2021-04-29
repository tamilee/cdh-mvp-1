from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search-results/', views.search, name='search'),
    path('search-results', views.search, name='search'),
    path('spacy_init', views.spacy_init, name='spacy_init'),
]
