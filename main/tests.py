from django.test import TestCase
from django.urls import reverse

from .models import JobApplication, JobPosting


class JobBoardTests(TestCase):
    def setUp(self):
        self.job = JobPosting.objects.create(
            title="Python разработчик",
            company_name="Зелена компания",
            location="София",
            work_mode=JobPosting.WorkMode.HYBRID,
            salary="1500 €",
            description="Работа с Django",
        )

    def test_home_shows_job_posting(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python разработчик")
        self.assertContains(response, "Зелена компания")

    def test_search_filters_by_title_only(self):
        response = self.client.get(
            reverse("home"), {"q": "Python"}
        )
        self.assertContains(response, "Python разработчик")
        self.assertEqual(len(response.context["jobs"]), 1)

        response = self.client.get(reverse("home"), {"q": "Django"})
        self.assertEqual(len(response.context["jobs"]), 0)

    def test_home_lists_city_counts_and_filters_selected_city(self):
        JobPosting.objects.create(
            title="Дизайнер",
            company_name="Студио",
            location="Пловдив",
            description="Дизайн",
        )
        response = self.client.get(reverse("home"), {"city": "Пловдив"})

        self.assertEqual([job.title for job in response.context["jobs"]], ["Дизайнер"])
        self.assertContains(response, "София")
        self.assertContains(response, "Пловдив")
        self.assertContains(response, "Всички градове")
        self.assertEqual(
            next(row["job_count"] for row in response.context["cities"] if row["location"] == "София"),
            1,
        )

    def test_job_detail_shows_description(self):
        response = self.client.get(reverse("job_detail", args=[self.job.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Работа с Django")

    def test_create_job_saves_and_redirects_to_detail(self):
        response = self.client.post(
            reverse("create_job"),
            {
                "title": "Дизайнер",
                "company_name": "Студио",
                "location": "София",
                "work_mode": JobPosting.WorkMode.REMOTE,
                "salary": "",
                "description": "Създаване на дигитални продукти.",
            },
        )

        created_job = JobPosting.objects.get(title="Дизайнер")
        self.assertRedirects(
            response, reverse("job_detail", args=[created_job.pk])
        )

    def test_edit_job_updates_existing_posting(self):
        response = self.client.post(
            reverse("edit_job", args=[self.job.pk]),
            {
                "title": "Старши Python разработчик",
                "company_name": "Зелена компания",
                "location": "Варна",
                "work_mode": JobPosting.WorkMode.REMOTE,
                "salary": "2000 €",
                "description": "Работа с Django",
            },
        )

        self.job.refresh_from_db()
        self.assertEqual(self.job.title, "Старши Python разработчик")
        self.assertEqual(self.job.location, "Варна")
        self.assertRedirects(
            response, reverse("job_detail", args=[self.job.pk])
        )

    def test_delete_requires_confirmation_then_deletes_on_post(self):
        confirmation = self.client.get(reverse("delete_job", args=[self.job.pk]))
        self.assertEqual(confirmation.status_code, 200)
        self.assertContains(confirmation, "Сигурни ли сте")
        self.assertTrue(JobPosting.objects.filter(pk=self.job.pk).exists())

        response = self.client.post(reverse("delete_job", args=[self.job.pk]))
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(JobPosting.objects.filter(pk=self.job.pk).exists())

    def test_missing_job_returns_404(self):
        response = self.client.get(reverse("job_detail", args=[9999]))

        self.assertEqual(response.status_code, 404)

    def test_application_is_saved_for_selected_job(self):
        response = self.client.post(
            reverse("apply_for_job", args=[self.job.pk]),
            {
                "full_name": "Мария Иванова",
                "email": "maria@example.com",
                "profile_url": "https://example.com/maria",
                "message": "Имам опит с Django.",
            },
        )

        application = JobApplication.objects.get()
        self.assertEqual(application.job, self.job)
        self.assertEqual(application.email, "maria@example.com")
        self.assertRedirects(
            response, f"{reverse('job_detail', args=[self.job.pk])}#apply"
        )

    def test_invalid_application_displays_form_errors(self):
        response = self.client.post(
            reverse("apply_for_job", args=[self.job.pk]),
            {"full_name": "", "email": "not-an-email", "message": ""},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(JobApplication.objects.count(), 0)
        self.assertContains(response, "Това поле е задължително.", status_code=400)
