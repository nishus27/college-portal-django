"""
URL configuration for college_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from notices import views as notice_views
from grievance import views as grievance_views
 

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login_view),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view),
    path('dashboard/',views.dashboard_view),
    path('profile/', views.profile_view, name='profile'),
    path("chatbot/", views.chatbot_view, name="chatbot"),
    path("teacher/notes/", views.teacher_notes, name="teacher_notes"),
    path("teacher/notes/edit/<int:note_id>/", views.edit_note, name="edit_note"),
    path("teacher/notes/delete/<int:note_id>/", views.delete_note, name="delete_note"),
    path("student/notes/", views.student_notes, name="student_notes"),
    path("notes/", views.notes_list, name="notes_list"),
    # ===== NOTICE ROUTES =====
    path('notices/',notice_views.notices_home, name='notices_home'),
    path('teacher/notices/', notice_views.teacher_notice_list, name='teacher_notice_list'),
    path('teacher/notices/create/', notice_views.teacher_notice_create, name='teacher_notice_create'),
    path('student/notices/', notice_views.student_notice_list, name='student_notice_list'),

     


    path('logout/', views.logout_view),
    
     
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    # Student
    path('student/grievances/', grievance_views.student_grievance_list, name='student_grievance_list'),
    path('student/grievances/create/', grievance_views.student_grievance_create, name='student_grievance_create'),
    path('student/grievances/edit/<int:grievance_id>/', grievance_views.student_grievance_edit, name='student_grievance_edit'),
    path('student/grievances/delete/<int:grievance_id>/', grievance_views.student_grievance_delete, name='student_grievance_delete'),

    # Teacher
    path('teacher/grievances/', grievance_views.teacher_grievance_list, name='teacher_grievance_list'),
    path('teacher/grievances/reply/<int:grievance_id>/', grievance_views.teacher_grievance_reply, name='teacher_grievance_reply'),
]