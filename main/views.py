from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import JobApplicationForm, JobPostingForm
from .models import JobPosting


def home(request):
    jobs = JobPosting.objects.all().order_by("-created_at")
    query = request.GET.get("q", "").strip()
    city = request.GET.get("city", "").strip()

    if query:
        jobs = jobs.filter(title__icontains=query)
    if city:
        jobs = jobs.filter(location=city)

    cities = JobPosting.objects.values("location").annotate(
        job_count=Count("id")
    ).order_by("location")

    return render(
        request,
        "main/home.html",
        {
            "jobs": jobs,
            "query": query,
            "city": city,
            "cities": cities,
            "total_jobs": JobPosting.objects.count(),
        },
    )


def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    return render(
        request,
        "main/job_detail.html",
        {"job": job, "application_form": JobApplicationForm()},
    )


def apply_for_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if request.method != "POST":
        return redirect("job_detail", pk=job.pk)

    form = JobApplicationForm(request.POST)
    if form.is_valid():
        application = form.save(commit=False)
        application.job = job
        application.save()
        messages.success(request, "Кандидатурата ти е изпратена. Успех!")
        return redirect(f"{reverse('job_detail', args=[job.pk])}#apply")

    return render(
        request,
        "main/job_detail.html",
        {"job": job, "application_form": form},
        status=400,
    )


def create_job(request):
    if request.method == "POST":
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect("job_detail", pk=job.pk)
    else:
        form = JobPostingForm()

    return render(request, "main/job_form.html", {"form": form})


def edit_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if request.method == "POST":
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Обявата е редактирана успешно.")
            return redirect("job_detail", pk=job.pk)
    else:
        form = JobPostingForm(instance=job)

    return render(
        request, "main/job_form.html", {"form": form, "job": job, "editing": True}
    )


def delete_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Обявата е изтрита.")
        return redirect("home")

    return render(request, "main/job_confirm_delete.html", {"job": job})
