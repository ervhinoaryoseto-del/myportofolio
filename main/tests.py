from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="AirGuard",
            description="SaaS untuk skrining risiko ISPA di kawasan rawan karhutla.",
            year=2026,
            category="competition",
            technologies="Python, Django",
            project_url="https://github.com/ervhinoaryoseto-del/airguard",
            is_featured=True,
        )

    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_projects_named_url_resolves(self):
        self.assertEqual(reverse("main:projects"), "/projects/")

    def test_project_model_str(self):
        self.assertEqual(str(self.project), "AirGuard")

    def test_project_appears_when_data_exists(self):
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "Competition")
        self.assertContains(response, "2026")

    def test_project_technologies_are_rendered(self):
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "Python")
        self.assertContains(response, "Django")

    def test_featured_project_shows_badge(self):
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "Featured")

    def test_project_url_link_shown_when_available(self):
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, self.project.project_url)

    def test_multiple_projects_all_render(self):
        Project.objects.create(
            title="Personal Portfolio",
            description="Website portofolio pribadi berbasis Django.",
            year=2026,
            category="personal",
        )
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "AirGuard")
        self.assertContains(response, "Personal Portfolio")

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:projects"))

        self.assertContains(response, "Belum ada project yang ditambahkan.")

    def test_navbar_links_to_projects(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, f'href="{reverse("main:projects")}"')
