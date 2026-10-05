from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_projects,
    create_project,
    get_projects_json,
    delete_project,
    update_project,
    create_experience,
    get_experiences_json,
    delete_experience,
    update_experience,
    register,
    login_user,
    logout_user,
    toggle_star,
    create_project_ajax,
    toggle_experience_star,
    create_experience_ajax,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("register/", register, name="register"),   
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),
    path("experience/<uuid:experience_id>/star/", toggle_experience_star, name="toggle_experience_star"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
]