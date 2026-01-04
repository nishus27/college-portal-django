from django.urls import path
from .views import *

urlpatterns = [
    path('', notices_home, name='notices_home'),
    path('teacher_notice_create', teacher_notice_create, name='teacher_notice_create'),
    path('teacher_notice_list', teacher_notice_list, name='teacher_notice_list'),
    path('student_notice_list', student_notice_list, name='student_notice_list'),
]
 