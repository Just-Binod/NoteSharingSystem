from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

from .views import custom_page_not_found
from .views import delete_user
##
from  nssapp import views as exclusive_views
##


urlpatterns = [
    
    path('nav/',views.nav,name='nav'),

    path('auth/google/', views.google_auth, name='google_login'),
    path('auth/google/callback/', views.google_auth_callback, name='google_callback'),


    path('auth/google/callback/debug/', views.debug_callback, name='debug_callback'),  # Temporary



    path('usernav/',views.usernav,name='usernav'),
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('register/',views.register_user,name='register'),
    path('login/',views.login_view,name='login'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
   path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('logout/',views.logout_view,name='logout'),
    path('note/dashboard/', views.dashboard_view, name='dashboard'),

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
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_profile1/', views.edit_profile1, name='edit_profile1'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('add_category/', views.add_category, name='add_category'),
    path("view-users/", views.view_users, name="view_users"),
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_complete"),

    path("note/<int:note_id>/", views.note_detail, name="note_detail"),
    path("note_admin/<int:note_id>/", views.note_detail_admin, name="note_detail_admin"),
    path("note/<int:note_id>/upvote/", views.upvote_note, name="upvote_note"),
    path("note/<int:note_id>/comment/", views.add_comment, name="add_comment"),
    path("note_admin/<int:note_id>/upvote/", views.upvote_note_admin, name="upvote_note_admin"),
    path("note_admin/<int:note_id>/comment/", views.add_comment_admin, name="add_comment_admin"),


    # exclusive
    # User exclusive notes URLs
    path('exclusive-notes/', exclusive_views.exclusive_notes_list, name='exclusive_notes_list'),
    path('purchase-note/<int:note_id>/', exclusive_views.purchase_note, name='purchase_note'),
    path('download-exclusive-note/<int:note_id>/', exclusive_views.download_exclusive_note, name='download_exclusive_note'),
    
    # Admin exclusive notes URLs
    path('admin/exclusive-notes/', exclusive_views.admin_exclusive_notes, name='admin_exclusive_notes'),
    path('admin/upload-exclusive-note/', exclusive_views.upload_exclusive_note, name='upload_exclusive_note'),
    path('admin/purchase-details/', exclusive_views.view_purchase_details, name='view_purchase_details'),




   
#    path('edit_profile/', views.edit_profile, name='edit_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# outside
handler404 = custom_page_not_found