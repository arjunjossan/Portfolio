from django.urls import path

from . import views

app_name = "portfolio_app"

urlpatterns = [
    path("", views.home, name="home"),
    path("unsubscribe/<uuid:token>/", views.unsubscribe, name="unsubscribe"),
    path("dashboard/login/", views.DashboardLoginView.as_view(), name="dashboard_login"),
    path("dashboard/logout/", views.DashboardLogoutView.as_view(), name="dashboard_logout"),
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    path("dashboard/<slug:section_slug>/", views.dashboard_section_list, name="dashboard_section"),
    path("dashboard/<slug:section_slug>/new/", views.dashboard_section_create, name="dashboard_create"),
    path("dashboard/<slug:section_slug>/<int:pk>/edit/", views.dashboard_section_edit, name="dashboard_edit"),
    path("dashboard/<slug:section_slug>/<int:pk>/delete/", views.dashboard_section_delete, name="dashboard_delete"),
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
