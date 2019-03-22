from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movies, name='movie'),
    path('movies/<str:arg0>/', views.movies, name='movie'),
    path('movies/<str:arg0>/<str:arg1>', views.movies, name='movie'),
    path('comments/', views.comments, name='movie'),
    path('comments/<str:arg0>/', views.comments, name='movie'),
    path('comments/<str:arg0>/<str:arg1>', views.comments, name='movie'),
    path('top/', views.top, name='movie'),
]
