from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notice
from .utils import ai_summarize


@login_required
def notices_home(request):
    role = request.session.get('role')

    if role == 'TEACHER':
        return redirect('teacher_notice_list')
    elif role == 'STUDENT':
        return redirect('student_notice_list')

    return redirect('/dashboard/')


# ---------- TEACHER ----------
@login_required
def teacher_notice_create(request):
    if request.session.get('role') != 'TEACHER':
        return redirect('/dashboard/')

    if request.method == 'POST':
        notice = Notice.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            category=request.POST['category'],
            attachment=request.FILES.get('attachment'),
            created_by=request.user
        )

        notice.ai_summary = ai_summarize(notice.description)
        notice.save()

        return redirect('teacher_notice_list')

    return render(request, 'notices/teacher_notice_create.html')


@login_required
def teacher_notice_list(request):
    if request.session.get('role') != 'TEACHER':
        return redirect('/dashboard/')

    notices = Notice.objects.filter(created_by=request.user)
    return render(request, 'notices/teacher_notice_list.html', {'notices': notices})


# ---------- STUDENT ----------
@login_required
def student_notice_list(request):
    if request.session.get('role') != 'STUDENT':
        return redirect('/dashboard/')

    notices = Notice.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'notices/student_notice_list.html', {'notices': notices})
 