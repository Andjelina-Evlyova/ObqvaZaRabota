"""
URL configuration for djangoproject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('jobs/new/', views.create_job, name='create_job'),
    path('jobs/<int:pk>/apply/', views.apply_for_job, name='apply_for_job'),
    path('jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
]