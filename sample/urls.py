from django.urls import path
from . import views

urlpatterns = [
    path('', views.sample_page, name='sample_page'),
    path('parts/', views.replacement_parts_page, name='replacement_parts_page'),
    path('parts/add/', views.add_replacement_part_view, name='add_replacement_part'),
]
