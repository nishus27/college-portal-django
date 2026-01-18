from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
import os
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from openai import OpenAI

 

#Register logic
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if not all([username, email, password, confirm_password, role]):
            return render(request, 'accounts/register.html', {
                'error': 'All fields are required'
            })

        if password != confirm_password:
            return render(request, 'accounts/register.html', {
                'error': 'Passwords do not match'
            })

        if role not in ['STUDENT', 'TEACHER']:
            return render(request, 'accounts/register.html', {
                'error': 'Invalid role'
            })

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('/login/')

        except IntegrityError:
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists'
            })

    return render(request, 'accounts/register.html')
 
 
#LOgin Logic
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not all([username, password, role]):
            return render(request, 'accounts/login.html', {
                'error': 'All fields are required'
            })

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

        if role not in ['STUDENT', 'TEACHER']:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid role'
            })

        login(request, user)
        request.session['role'] = role
        return redirect('/dashboard/')

    return render(request, 'accounts/login.html')
 
 
 
#Logout Logic
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/login/')
 
#Dashboard logic
@login_required
def dashboard_view(request):
    role = request.session.get('role')

    if role == 'STUDENT':
        return render(request, 'dashboards/student_dashboard.html')

    elif role == 'TEACHER':
        return render(request, 'dashboards/teacher_dashboard.html')

    else:
        # fallback (future admin)
        return redirect('/login/')
 
#Profile View 
@login_required
def profile_view(request):
    role = request.session.get('role', 'STUDENT')

    # Load existing session data
    full_name = request.session.get('full_name', '')
    year = request.session.get('year', '')
    branch = request.session.get('branch', '')
    profile_pic = request.session.get('profile_pic')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        branch = request.POST.get('branch')

        request.session['full_name'] = full_name
        request.session['branch'] = branch

        if role == 'STUDENT':
            year = request.POST.get('year')
            request.session['year'] = year

        # Handle profile picture upload
        if 'profile_pic' in request.FILES:
            pic = request.FILES['profile_pic']
            pic_path = os.path.join('profiles', pic.name)

            full_path = os.path.join(settings.MEDIA_ROOT, pic_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'wb+') as f:
                for chunk in pic.chunks():
                    f.write(chunk)

            request.session['profile_pic'] = settings.MEDIA_URL + pic_path

    profile_pic_url = profile_pic if profile_pic else settings.STATIC_URL + 'images/default_profile.png'

    context = {
        'role': role,
        'full_name': full_name,
        'year': year,
        'branch': branch,
        'profile_pic_url': profile_pic_url,
    }

    return render(request, 'profile/profile.html', context)

#ChatBot View
@login_required
def chatbot_view(request):
    if request.method == "GET":
        return render(request, "chatbot/chatbot.html")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").strip()

            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            if not message:
                return JsonResponse({"reply": "Please type a message."})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful academic assistant for college students."},
                    {"role": "user", "content": message}
                ],
                max_tokens=300
            )

            return JsonResponse({
                "reply": response.choices[0].message.content
            })

        except Exception as e:
            print("❌ OpenAI Error:", e)
            return JsonResponse({
                "reply": "AI service unavailable. Please try later."
            })
 
#Teacher Notes 
from notes.models import Note


@login_required
def teacher_notes(request):
    if request.method == "POST":
        pdf = request.FILES.get("pdf")
        title = request.POST.get("title")

        if pdf and title:
            Note.objects.create(
                title=title,
                pdf=pdf,
                uploaded_by=request.user
            )

        return redirect("teacher_notes")

    notes = Note.objects.filter(uploaded_by=request.user).order_by("-uploaded_at")

    return render(request, "notes/teacher_notes.html", {
        "notes": notes
    })


@login_required
def student_notes(request):
    notes = Note.objects.all().order_by("-uploaded_at")

    return render(request, "notes/student_notes.html", {
        "notes": notes
    })
 


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, uploaded_by=request.user)

    if request.method == "POST":
        note.title = request.POST.get("title")

        if request.FILES.get("pdf"):
            note.pdf = request.FILES.get("pdf")

        note.save()
        return redirect("teacher_notes")

    return render(request, "notes/edit_note.html", {
        "note": note
    })


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, uploaded_by=request.user)

    if request.method == "POST":
        note.delete()
        return redirect("teacher_notes")

    return render(request, "notes/delete_note.html", {
        "note": note
    }) 


#Notes list
@login_required
def notes_list(request):
    search_query = request.GET.get("q", "")

    notes = Note.objects.all().order_by("-uploaded_at")

    if search_query:
        notes = notes.filter(
            Q(title__icontains=search_query)
        )

    paginator = Paginator(notes, 5)  # 5 notes per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "notes/notes_list.html", {
        "page_obj": page_obj,
        "search_query": search_query
    })
