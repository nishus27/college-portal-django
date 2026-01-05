from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from . import views
from notices import views as notice_views
from grievance import views as grievance_views

urlpatterns = [
    # Root
    path('', lambda request: redirect('login'), name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard & profile
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),

    # Chatbot
    path('chatbot/', views.chatbot_view, name='chatbot'),

    # Notes
    path('teacher/notes/', views.teacher_notes, name='teacher_notes'),
    path('teacher/notes/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('teacher/notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('student/notes/', views.student_notes, name='student_notes'),
    path('notes/', views.notes_list, name='notes_list'),

    # Notices
    path('notices/', notice_views.notices_home, name='notices_home'),
    path('teacher/notices/', notice_views.teacher_notice_list, name='teacher_notice_list'),
    path('teacher/notices/create/', notice_views.teacher_notice_create, name='teacher_notice_create'),
    path('student/notices/', notice_views.student_notice_list, name='student_notice_list'),

    # Grievances – Student
    path('student/grievances/', grievance_views.student_grievance_list, name='student_grievance_list'),
    path('student/grievances/create/', grievance_views.student_grievance_create, name='student_grievance_create'),
    path('student/grievances/edit/<int:grievance_id>/', grievance_views.student_grievance_edit, name='student_grievance_edit'),
    path('student/grievances/delete/<int:grievance_id>/', grievance_views.student_grievance_delete, name='student_grievance_delete'),

    # Grievances – Teacher
    path('teacher/grievances/', grievance_views.teacher_grievance_list, name='teacher_grievance_list'),
    path('teacher/grievances/reply/<int:grievance_id>/', grievance_views.teacher_grievance_reply, name='teacher_grievance_reply'),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 