from django.shortcuts import render

from main.models import Experience


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