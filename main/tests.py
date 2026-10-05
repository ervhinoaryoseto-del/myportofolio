"""Test suite untuk portofolio.

Cakupan:
- Halaman kerangka (Experience & Projects) yang datanya dimuat lewat AJAX
- Endpoint JSON (data, info star, pencarian)
- Endpoint POST AJAX: status 201 / 400 / 403 / 405 dan perlindungan XSS
- Hak akses per peran: pengunjung, user biasa, Editor, superuser
- Toggle star dan regresi form edit
"""
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import ExperienceForm
from main.models import Experience, Project


class RoleTestCase(TestCase):
    """Base class: menyiapkan satu akun untuk tiap peran."""

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser("owner", password="pw-owner-123")
        cls.editor = User.objects.create_user("editor", password="pw-editor-123")
        cls.editor.groups.add(Group.objects.create(name="Editor"))
        cls.member = User.objects.create_user("member", password="pw-member-123")

    def as_user(self, user):
        self.client.force_login(user)
        return self.client


class MainTest(TestCase):
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        self.assertEqual(self.client.get("/halaman-yang-tidak-ada/").status_code, 404)


class ExperiencePageTest(TestCase):
    """Halaman Experience hanya kerangka; data datang dari endpoint JSON."""

    def test_page_renders_skeleton_only(self):
        Experience.objects.create(title="Asisten Dosen PBP", description="Membantu mahasiswa.")
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, reverse("main:get_experiences_json"))
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="error"')
        # Data tidak boleh ada di HTML awal, hanya lewat fetch()
        self.assertNotContains(response, "Asisten Dosen PBP")

    def test_add_button_and_modal_only_for_superuser(self):
        owner = User.objects.create_superuser("owner", password="x12345678!")
        member = User.objects.create_user("member", password="x12345678!")
        url = reverse("main:show_experience")

        modal = 'id="add-experience-modal"'
        self.assertNotContains(self.client.get(url), modal)
        self.client.force_login(member)
        self.assertNotContains(self.client.get(url), modal)
        self.client.force_login(owner)
        self.assertContains(self.client.get(url), modal)


class ExperienceModelTest(TestCase):
    def test_str_and_is_ongoing(self):
        exp = Experience.objects.create(title="Magang", description="d", category="internship")
        self.assertEqual(str(exp), "Magang")
        self.assertTrue(exp.is_ongoing)

        exp.ended_at = timezone.now()
        exp.save()
        self.assertFalse(exp.is_ongoing)


class ExperienceJsonTest(RoleTestCase):
    def setUp(self):
        self.exp = Experience.objects.create(
            title="Asisten Dosen PBP", description="Membantu mahasiswa.", category="part-time"
        )
        Experience.objects.create(title="Riset AirGuard", description="Riset.", category="research")
        self.url = reverse("main:get_experiences_json")

    def test_visitor_can_read_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_json_contains_star_info_for_visitor(self):
        fields = self.client.get(self.url, {"title": "PBP"}).json()[0]["fields"]

        self.assertEqual(fields["star_count"], 0)
        self.assertFalse(fields["is_starred"])
        self.assertEqual(fields["category_display"], "Part-Time")
        self.assertTrue(fields["is_ongoing"])

    def test_json_reports_star_state_of_logged_in_user(self):
        self.exp.starred_by.add(self.member)

        as_member = self.as_user(self.member).get(self.url, {"title": "PBP"}).json()[0]["fields"]
        self.assertEqual(as_member["star_count"], 1)
        self.assertTrue(as_member["is_starred"])
        self.assertEqual(as_member["starred_by_names"], "member")

        as_owner = self.as_user(self.owner).get(self.url, {"title": "PBP"}).json()[0]["fields"]
        self.assertEqual(as_owner["star_count"], 1)
        self.assertFalse(as_owner["is_starred"])

    def test_search_filters_by_title(self):
        data = self.client.get(self.url, {"title": "airguard"}).json()
        self.assertEqual([d["fields"]["title"] for d in data], ["Riset AirGuard"])

    def test_search_without_result_returns_empty_list(self):
        self.assertEqual(self.client.get(self.url, {"title": "zzzz"}).json(), [])

    def test_json_does_not_expose_user_ids(self):
        self.exp.starred_by.add(self.member)
        body = self.client.get(self.url, {"title": "PBP"}).content.decode()
        self.assertNotIn('"starred_by":', body)


class CreateExperienceAjaxTest(RoleTestCase):
    def setUp(self):
        self.url = reverse("main:create_experience_ajax")
        self.payload = {"title": "Magang Data", "description": "Analisis data.", "category": "internship"}

    def test_visitor_gets_403_json(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, 403)
        self.assertIn("message", response.json())

    def test_regular_user_gets_403(self):
        self.assertEqual(self.as_user(self.member).post(self.url, self.payload).status_code, 403)

    def test_editor_cannot_create(self):
        response = self.as_user(self.editor).post(self.url, self.payload)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Experience.objects.exists())

    def test_owner_creates_with_201(self):
        response = self.as_user(self.owner).post(self.url, self.payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.get().title, "Magang Data")
        self.assertEqual(response.json()["pk"], str(Experience.objects.get().pk))

    def test_blank_title_returns_400_with_errors(self):
        response = self.as_user(self.owner).post(self.url, {**self.payload, "title": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertFalse(Experience.objects.exists())

    def test_invalid_thumbnail_url_is_rejected(self):
        response = self.as_user(self.owner).post(
            self.url, {**self.payload, "thumbnail": "javascript:alert(1)"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("thumbnail", response.json()["errors"])

    def test_get_is_not_allowed(self):
        self.assertEqual(self.as_user(self.owner).get(self.url).status_code, 405)

    def test_csrf_is_enforced(self):
        from django.test import Client

        strict = Client(enforce_csrf_checks=True)
        strict.force_login(self.owner)
        self.assertEqual(strict.post(self.url, self.payload).status_code, 403)
        self.assertFalse(Experience.objects.exists())


class XssProtectionTest(RoleTestCase):
    url_name = "main:create_experience_ajax"

    def test_html_only_title_is_rejected(self):
        payload = {
            "title": '<img src="x" onerror="alert(\'XSS!\')">',
            "description": "d",
            "category": "research",
        }
        response = self.as_user(self.owner).post(reverse(self.url_name), payload)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Experience.objects.exists())

    def test_tags_are_stripped_from_title_and_description(self):
        payload = {
            "title": "Halo <b>dunia</b>",
            "description": "<script>alert(1)</script>Deskripsi",
            "category": "research",
        }
        self.as_user(self.owner).post(reverse(self.url_name), payload)

        exp = Experience.objects.get()
        self.assertEqual(exp.title, "Halo dunia")
        self.assertNotIn("<", exp.description)

    def test_project_form_sanitizes_technologies(self):
        from main.forms import ProjectForm

        form = ProjectForm(
            {"title": "P", "description": "d", "year": 2026, "category": "personal",
             "technologies": "<b>Django</b>, Python"}
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["technologies"], "Django, Python")


class ExperiencePermissionTest(RoleTestCase):
    def setUp(self):
        self.exp = Experience.objects.create(
            title="Asisten", description="d", category="part-time", ended_at=timezone.now()
        )
        self.edit_url = reverse("main:update_experience", args=[self.exp.id])
        self.delete_url = reverse("main:delete_experience", args=[self.exp.id])

    def test_visitor_is_redirected_to_login(self):
        for url in (self.edit_url, self.delete_url, reverse("main:create_experience")):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login/", response["Location"])

    def test_regular_user_cannot_edit_or_delete(self):
        client = self.as_user(self.member)
        self.assertEqual(client.get(self.edit_url).status_code, 403)
        self.assertEqual(client.post(self.delete_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.exp.pk).exists())

    def test_editor_can_edit_but_not_create_or_delete(self):
        client = self.as_user(self.editor)
        self.assertEqual(client.get(self.edit_url).status_code, 200)
        self.assertEqual(client.get(reverse("main:create_experience")).status_code, 403)
        self.assertEqual(client.post(self.delete_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.exp.pk).exists())

    def test_editor_update_is_saved(self):
        response = self.as_user(self.editor).post(
            self.edit_url,
            {"title": "Asisten Dosen", "description": "baru", "category": "part-time",
             "ended_at": "2026-10-04T10:30"},
        )
        self.assertEqual(response.status_code, 302)
        self.exp.refresh_from_db()
        self.assertEqual(self.exp.title, "Asisten Dosen")
        self.assertIsNotNone(self.exp.ended_at)

    def test_owner_can_delete(self):
        response = self.as_user(self.owner).post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Experience.objects.filter(pk=self.exp.pk).exists())

    def test_edit_form_prefills_ended_at_in_datetime_local_format(self):
        """Regresi: nilai awal harus berformat YYYY-MM-DDTHH:MM agar tampil di input datetime-local.

        Jika formatnya salah, browser mengosongkan input dan mengedit experience
        yang sudah selesai akan menghapus ended_at.
        """
        html = str(ExperienceForm(instance=self.exp)["ended_at"])
        expected = timezone.localtime(self.exp.ended_at).strftime("%Y-%m-%dT%H:%M")
        self.assertIn(f'value="{expected}"', html)


class ExperienceStarTest(RoleTestCase):
    def setUp(self):
        self.exp = Experience.objects.create(title="Asisten", description="d")
        self.url = reverse("main:toggle_experience_star", args=[self.exp.id])

    def test_visitor_is_redirected_to_login(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])
        self.assertEqual(self.exp.starred_by.count(), 0)

    def test_user_can_star_and_unstar(self):
        client = self.as_user(self.member)
        client.post(self.url)
        self.assertEqual(self.exp.starred_by.count(), 1)
        client.post(self.url)
        self.assertEqual(self.exp.starred_by.count(), 0)

    def test_get_does_not_change_star(self):
        self.as_user(self.member).get(self.url)
        self.assertEqual(self.exp.starred_by.count(), 0)


class ProjectTest(RoleTestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="AirGuard",
            description="SaaS untuk skrining risiko ISPA.",
            year=2026,
            category="competition",
            technologies="Python, Django",
            project_url="https://example.com/airguard",
            is_featured=True,
        )

    def test_named_url_resolves(self):
        self.assertEqual(reverse("main:show_projects"), "/projects/")

    def test_page_renders_skeleton_with_featured_badge_support(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, reverse("main:get_projects_json"))
        self.assertContains(response, "project-featured-badge")
        self.assertNotContains(response, "AirGuard")

    def test_model_str_and_technology_list(self):
        self.assertEqual(str(self.project), "AirGuard")
        self.assertEqual(self.project.technology_list, ["Python", "Django"])

    def test_json_contains_project_data_and_star_info(self):
        self.project.starred_by.add(self.member)
        fields = self.as_user(self.member).get(reverse("main:get_projects_json")).json()[0]["fields"]

        self.assertEqual(fields["title"], "AirGuard")
        self.assertTrue(fields["is_featured"])
        self.assertEqual(fields["star_count"], 1)
        self.assertTrue(fields["is_starred"])

    def test_project_search(self):
        url = reverse("main:get_projects_json")
        self.assertEqual(len(self.client.get(url, {"title": "air"}).json()), 1)
        self.assertEqual(self.client.get(url, {"title": "zzzz"}).json(), [])

    def test_create_project_ajax_roles(self):
        url = reverse("main:create_project_ajax")
        payload = {"title": "Baru", "description": "d", "year": 2026, "category": "personal"}

        self.assertEqual(self.client.post(url, payload).status_code, 403)
        self.assertEqual(self.as_user(self.member).post(url, payload).status_code, 403)
        self.assertEqual(self.as_user(self.editor).post(url, payload).status_code, 403)
        self.assertEqual(self.as_user(self.owner).post(url, payload).status_code, 201)
        self.assertEqual(self.as_user(self.owner).post(url, {**payload, "title": " "}).status_code, 400)

    def test_editor_can_edit_but_not_delete_project(self):
        client = self.as_user(self.editor)
        self.assertEqual(client.get(reverse("main:update_project", args=[self.project.id])).status_code, 200)
        self.assertEqual(client.post(reverse("main:delete_project", args=[self.project.id])).status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
