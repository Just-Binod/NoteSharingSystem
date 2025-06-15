from django.contrib import admin
from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('nav/',views.nav,name='nav'),
    path('home/',views.home,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('profile/',views.profile,name='profile'),
    # path('create/', views.create_note, name='create_note'),
    # path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    # path('notes/', views.note_list, name='note_list'),
    path('upload_notes/', views.upload_notes, name='upload_notes'),
    path('viewmy_notes/', views.viewmy_notes, name='viewmy_notes'),
   path('delete_mynotes/<int:id>/',views.delete_mynotes,name='delete_mynotes'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
