from django.urls import path

from . import views

app_name = "portfolio_app"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("skills/", views.skills, name="skills"),
    path("projects/", views.projects_list, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("experience/", views.experience, name="experience"),
    path("education/", views.education, name="education"),
    path("contact/", views.contact, name="contact"),
    path("resume/", views.resume, name="resume"),
    path("api/projects/filter/", views.filter_projects, name="filter_projects"),
    path("api/skills/search/", views.search_skills, name="search_skills"),
    path("404/", views.page_not_found, name="404"),
]
