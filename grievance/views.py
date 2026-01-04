# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Grievance

# ---------- STUDENT ----------

@login_required
def student_grievance_list(request):
    if request.session.get('role') != 'STUDENT':
        return redirect('/dashboard/')

    grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'grievance/student_grievance_list.html', {
        'grievances': grievances
    })


@login_required
def student_grievance_create(request):
    if request.session.get('role') != 'STUDENT':
        return redirect('/dashboard/')

    if request.method == 'POST':
        Grievance.objects.create(
            student=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            attachment=request.FILES.get('attachment')
        )
        return redirect('student_grievance_list')

    return render(request, 'grievance/student_grievance_create.html')


@login_required
def student_grievance_edit(request, grievance_id):
    grievance = get_object_or_404(Grievance, id=grievance_id, student=request.user)

    if grievance.status != 'PENDING':
        return redirect('student_grievance_list')

    if request.method == 'POST':
        grievance.title = request.POST['title']
        grievance.description = request.POST['description']
        grievance.save()
        return redirect('student_grievance_list')

    return render(request, 'grievance/student_grievance_edit.html', {
        'grievance': grievance
    })


@login_required
def student_grievance_delete(request, grievance_id):
    grievance = get_object_or_404(Grievance, id=grievance_id, student=request.user)

    if grievance.status == 'PENDING':
        grievance.delete()

    return redirect('student_grievance_list')


# ---------- TEACHER ----------

@login_required
def teacher_grievance_list(request):
    if request.session.get('role') != 'TEACHER':
        return redirect('/dashboard/')

    grievances = Grievance.objects.all().order_by('-created_at')
    return render(request, 'grievance/teacher_grievance_list.html', {
        'grievances': grievances
    })


@login_required
def teacher_grievance_reply(request, grievance_id):
    if request.session.get('role') != 'TEACHER':
        return redirect('/dashboard/')

    grievance = get_object_or_404(Grievance, id=grievance_id)

    if request.method == 'POST':
        grievance.reply = request.POST['reply']
        grievance.status = 'REPLIED'
        grievance.save()
        return redirect('teacher_grievance_list')

    return render(request, 'grievance/teacher_grievance_reply.html', {
        'grievance': grievance
    })
