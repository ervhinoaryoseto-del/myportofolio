import uuid
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('competition', 'Competition'),
        ('organization', 'Organization'),
        ('academic', 'Academic'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.PositiveSmallIntegerField(help_text="Tahun project dikerjakan atau dimulai.")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    technologies = models.CharField(
        max_length=255,
        blank=True,
        help_text="Daftar teknologi dipisahkan koma, contoh: Django, React, Figma.",
    )
    project_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_featured', '-year', 'title']

    def __str__(self):
        return self.title

    @property
    def technology_list(self):
        """Return the comma-separated technologies string as a clean list for the template."""
        if not self.technologies:
            return []
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]