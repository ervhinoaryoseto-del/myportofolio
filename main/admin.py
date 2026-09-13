from django.contrib import admin
from main.models import Experience, Project

# Register your models here. 
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_ongoing")
    list_filter = ("category",)
 
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "year", "is_featured")
    list_filter = ("category", "is_featured", "year")
    ordering = ("-is_featured", "-year", "title")