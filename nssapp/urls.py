from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    
    path('nav/',views.nav,name='nav'),
    path('home/',views.home,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('adminpage/',views.adminpage,name='adminpage'),

]
