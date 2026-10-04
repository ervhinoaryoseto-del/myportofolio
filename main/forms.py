from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput
from main.models import Project, Experience
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "year",
            "category",
            "technologies",
            "project_url",
            "image_url",
            "is_featured",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "year": "Tahun",
            "category": "Kategori",
            "technologies": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "image_url": "URL Gambar Proyek",
            "is_featured": "Tampilkan di Halaman Utama",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "technologies": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_technologies(self):
        return strip_tags(self.cleaned_data["technologies"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model =  Experience
        fields = [
            'title',
            'description',
            'category',
            'thumbnail',
            'ended_at',
        ] 

        labels = {
            'title': 'Nama Pengalaman',
            'description': 'Deskripsi',
            'category': 'Kategori',
            'thumbnail': 'URL Thumbnail',
            'ended_at': 'Tanggal Berakhir',
        }

        widgets = {
            'description': Textarea(attrs={
                'rows': 5,
                'placeholder': 'deskripsikan pengalamanmu'
            }),

            'ended_at': DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()