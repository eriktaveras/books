from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.book_list, name='book_list'),
    path('api/libros/', views.book_api, name='book_api'),
    path('api/search-suggestions/', views.search_suggestions_api, name='search_suggestions_api'),
    path('libros/nuevo/', views.book_create, name='book_create'),
    path('libros/<int:pk>/', views.book_detail, name='book_detail'),
    path('libros/<int:pk>/editar/', views.book_update, name='book_update'),
    path('dewey/', views.dewey_list, name='dewey_list'),
    path('api/dewey/', views.dewey_api, name='dewey_api'),
    path('dewey/nuevo/', views.dewey_create, name='dewey_create'),
    path('dewey/<int:pk>/editar/', views.dewey_update, name='dewey_update'),
] 