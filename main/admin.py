from django.contrib import admin

from .models import JobApplication, JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "location", "work_mode", "created_at")
    list_filter = ("location", "work_mode", "created_at")
    search_fields = ("title", "company_name", "location", "description")
    ordering = ("-created_at",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "email", "created_at")
    list_filter = ("created_at",)
    search_fields = ("full_name", "email", "job__title", "job__company_name")
    ordering = ("-created_at",)
