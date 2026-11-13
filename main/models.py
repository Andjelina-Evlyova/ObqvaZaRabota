from django.db import models


class JobPosting(models.Model):
    class WorkMode(models.TextChoices):
        ONSITE = "onsite", "На място"
        HYBRID = "hybrid", "Хибридно"
        REMOTE = "remote", "Дистанционно"

    title = models.CharField(max_length=250, verbose_name="Заглавие")
    company_name = models.CharField(max_length=150, verbose_name="Компания")
    location = models.CharField(max_length=100, verbose_name="Град")
    work_mode = models.CharField(
        max_length=10,
        choices=WorkMode.choices,
        default=WorkMode.ONSITE,
        verbose_name="Начин на работа",
    )
    salary = models.CharField(max_length=100, blank=True, null=True, verbose_name="Заплата")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return f"{self.title} - {self.company_name}"


class JobApplication(models.Model):
    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Обява",
    )
    full_name = models.CharField(max_length=150, verbose_name="Име и фамилия")
    email = models.EmailField(verbose_name="Имейл")
    profile_url = models.URLField(blank=True, verbose_name="Профил или CV линк")
    message = models.TextField(verbose_name="Кратко представяне")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return f"{self.full_name} — {self.job.title}"
