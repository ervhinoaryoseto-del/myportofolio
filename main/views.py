import datetime
from main.forms import ProjectForm, ExperienceForm
from main.models import Experience, Project

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts   import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Ervhino Aryo Seto",
        "npm": "2506551125",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at the University of Indonesia with an interest in Technology, Data, "
            "and Product Management. I enjoy exploring how technology can be used to solve real-world problems and create an impact."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Ervhino Aryo Seto",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Ervhino Aryo Seto",
        "form": form,
    }
    return render(request, "experience_form.html", context)


def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Ervhino Aryo Seto",
        "form": form,
        "experience": experience,
    }

    return render(request, "experience_form.html", context)

def is_editor_user(user):
    return user.is_authenticated and user.groups.filter(name__iexact='Editor').exists()


def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by")

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    starred_ids = set()
    if request.user.is_authenticated:
        starred_ids = set(request.user.starred_projects.values_list("pk", flat=True))

    context = {
        "name": "Ervhino Aryo Seto",
        "project_list": projects,
        "title_query": title_query,
        "is_editor": is_editor_user(request.user),
        "starred_ids": starred_ids,
    }
    return render(request, "projects.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Ervhino Aryo Seto",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize(
        "json",
        projects,
        fields=[
            "title", "description", "year", "category",
            "technologies", "project_url", "image_url", "is_featured",
        ],
    )
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/") 
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not request.user.is_superuser:
            raise PermissionDenied
    
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/") 
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not (request.user.is_superuser or is_editor_user(request.user)):
        return HttpResponseForbidden("Anda tidak memiliki akses untuk mengubah project ini.")
    
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "project berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Ervhino Aryo Seto",
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Ervhino Aryo Seto",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    
    context = {
        "name": "Ervhino Aryo Seto",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    response.delete_cookie('sessionid')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")