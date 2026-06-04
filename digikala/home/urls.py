from django.urls import path
from . import views


urlpatterns = [
    path('',views. home, name='home'),
    path('about/',views.about,name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('singup/',views.singup_user, name = 'singup'),
    path('product/<int:pk>',views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
]