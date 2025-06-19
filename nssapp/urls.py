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
    path('profile1/',views.profile1,name='profile1'),
    # path('create/', views.create_note, name='create_note'),
    # path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    # path('notes/', views.note_list, name='note_list'),
    path('notes_list/', views.notes_list, name='notes_list'),
    path('upload_notes/', views.upload_notes, name='upload_notes'),
    path('download_note/<int:pk>/', views.download_note, name='download_note'),
    path('viewmy_notes/', views.viewmy_notes, name='viewmy_notes'),
    path('viewall_notes/', views.viewall_notes, name='viewall_notes'),
    path('viewall_notes_user/', views.viewall_notes_user, name='viewall_notes_user'),
    path('delete_mynotes/<int:id>/',views.delete_mynotes,name='delete_mynotes'),
    path('delete_mynotes_admin/<int:id>/',views.delete_mynotes_admin,name='delete_mynotes_admin'),
    path('upload_notes_admin/', views.upload_notes_admin, name='upload_notes_admin'),
    path('viewmy_notes_admin/', views.viewmy_notes_admin, name='viewmy_notes_admin'),
   
#    path('edit_profile/', views.edit_profile, name='edit_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
