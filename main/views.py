from main.forms import ProjectForm
from main.models import Experience, Project

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts   import get_object_or_404, redirect, render

def show_main(request):
    context = {
        "name": "Ervhino Aryo Seto",
        "npm": "2506551125",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at the University of Indonesia with an interest in Technology, Data, "
            "and Product Management. I enjoy exploring how technology can be used to solve real-world problems and create an impact."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Ervhino Aryo Seto",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "name": "Ervhino Aryo Seto",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)


def create_project(request):
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

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

