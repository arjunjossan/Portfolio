from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import ContactSubmissionForm, SubscriberForm
from .models import (
    AboutSection,
    Certification,
    ContactInformation,
    Education,
    Experience,
    HeroSection,
    PageMetaData,
    Project,
    TechnicalSkill,
    Subscriber,
)


def grouped_skills():
    skills = TechnicalSkill.objects.filter(is_active=True).order_by("category", "-proficiency_level", "order", "skill_name")
    skill_groups = OrderedDict()
    for skill in skills:
        skill_groups.setdefault(skill.category, []).append(skill)
    return skill_groups


def page_meta(page_name, fallback_title, fallback_description):
    return PageMetaData.objects.filter(page_name=page_name).first() or {
        "meta_title": fallback_title,
        "meta_description": fallback_description,
        "meta_keywords": "",
        "og_description": fallback_description,
        "og_image": None,
    }


def base_page_context(page_name, title, description):
    return {
        "page_name": page_name,
        "page_meta": page_meta(page_name, title, description),
    }


def handle_contact_submission(request, success_redirect):
    form = ContactSubmissionForm(request.POST, request.FILES)
    if form.is_valid():
        submission = form.save()
        send_mail(
            subject=f"Portfolio contact: {submission.subject}",
            message=(
                f"From: {submission.name}\n"
                f"Email: {submission.email}\n"
                f"Phone: {submission.phone}\n"
                f"Company: {submission.company}\n"
                f"Type: {submission.message_type}\n\n"
                f"{submission.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
        messages.success(request, "Your message has been sent successfully.")
        if success_redirect == "portfolio_app:contact":
            return redirect(f"{reverse(success_redirect)}?submitted=1")
        return redirect(f"{reverse(success_redirect)}?contact_submitted=1#home-contact")
    messages.error(request, "Please review the form and fix the highlighted fields.")
    return form


def handle_subscriber_submission(request, success_redirect):
    form = SubscriberForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]
        anchor = request.POST.get("subscription_anchor", "subscribe-updates").strip() or "subscribe-updates"
        if anchor not in {"subscribe-updates", "footer-subscribe"}:
            anchor = "subscribe-updates"
        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={"is_active": True},
        )
        status = "subscribed"
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=["is_active"])
            status = "reactivated"
        elif not created and subscriber.is_active:
            status = "already_subscribed"
        return redirect(f"{reverse(success_redirect)}?subscription={status}&subscription_anchor={anchor}#{anchor}")
    messages.error(request, "Please enter a valid email address to subscribe.")
    return form


def home(request):
    subscribe_form = SubscriberForm()
    if request.method == "POST":
        if request.POST.get("form_type") == "subscribe":
            result = handle_subscriber_submission(request, "portfolio_app:home")
            if not isinstance(result, SubscriberForm):
                return result
            subscribe_form = result
            contact_form = ContactSubmissionForm()
        else:
            result = handle_contact_submission(request, "portfolio_app:home")
            if not isinstance(result, ContactSubmissionForm):
                return result
            contact_form = result
    else:
        contact_form = ContactSubmissionForm()

    hero = HeroSection.objects.filter(is_active=True).first()
    about = AboutSection.objects.filter(is_active=True).first()
    featured_projects = Project.objects.filter(is_active=True, is_featured=True).order_by("order", "-is_featured", "-start_date")[:3]
    if not featured_projects:
        featured_projects = Project.objects.filter(is_active=True).order_by("order", "-is_featured", "-start_date")[:3]

    context = {
        **base_page_context(
            "home",
            "Arjun Singh | Developer Portfolio",
            "Multi-page Django portfolio highlighting projects, skills, experience, and technical background.",
        ),
        "hero": hero,
        "about": about,
        "contact_info": ContactInformation.objects.filter(is_active=True).first(),
        "featured_projects": featured_projects,
        "skill_groups": grouped_skills(),
        "contact_form": contact_form,
        "subscribe_form": subscribe_form,
        "subscription_prompt": request.GET.get("subscription", "").strip(),
        "subscription_anchor": request.GET.get("subscription_anchor", "subscribe-updates").strip() or "subscribe-updates",
        "home_contact_success_prompt": request.GET.get("contact_submitted", "").strip() == "1",
    }
    return render(request, "home/index.html", context)


def about(request):
    context = {
        **base_page_context(
            "about",
            "About Arjun Singh",
            "Background, achievements, and professional goals of Arjun Singh.",
        ),
        "about": AboutSection.objects.filter(is_active=True).first(),
        "education_list": Education.objects.filter(is_active=True).order_by("order", "-end_date"),
        "breadcrumbs": [{"label": "About", "url": ""}],
    }
    return render(request, "about/about.html", context)


def skills(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "proficiency")

    skills_qs = TechnicalSkill.objects.filter(is_active=True)
    if query:
        skills_qs = skills_qs.filter(
            Q(skill_name__icontains=query) | Q(description__icontains=query)
        )
    if category:
        skills_qs = skills_qs.filter(category=category)

    if sort == "name":
        skills_qs = skills_qs.order_by("skill_name")
    elif sort == "experience":
        skills_qs = skills_qs.order_by("-years_of_experience", "-proficiency_level", "skill_name")
    else:
        skills_qs = skills_qs.order_by("category", "-proficiency_level", "-years_of_experience", "skill_name")

    grouped = OrderedDict()
    for skill in skills_qs:
        grouped.setdefault(skill.category, []).append(skill)

    context = {
        **base_page_context(
            "skills",
            "Technical Skills",
            "Detailed overview of Arjun Singh's backend, frontend, cloud, and data analysis skill set.",
        ),
        "skill_groups": grouped,
        "skill_categories": [choice[0] for choice in TechnicalSkill.SkillCategory.choices],
        "active_query": query,
        "active_category": category,
        "active_sort": sort,
        "breadcrumbs": [{"label": "Skills", "url": ""}],
    }
    return render(request, "skills/skills.html", context)


def projects_list(request):
    projects = Project.objects.filter(is_active=True)
    search = request.GET.get("q", "").strip()
    technology = request.GET.get("technology", "").strip()
    status = request.GET.get("status", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "custom")

    if search:
        projects = projects.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(detailed_description__icontains=search)
        )
    if technology:
        projects = projects.filter(technologies_used__icontains=technology)
    if status:
        projects = projects.filter(status=status)
    if category:
        projects = projects.filter(category=category)

    if sort == "oldest":
        projects = projects.order_by("start_date", "order")
    elif sort == "featured":
        projects = projects.order_by("-is_featured", "order", "-start_date")
    elif sort == "newest":
        projects = projects.order_by("-start_date", "order")
    else:
        projects = projects.order_by("order", "-is_featured", "-start_date")

    paginator = Paginator(projects, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        **base_page_context(
            "projects",
            "Projects Portfolio",
            "Browse Django, full-stack, and data-focused projects with filtering and detailed breakdowns.",
        ),
        "page_obj": page_obj,
        "projects": page_obj.object_list,
        "technology_options": sorted(
            {tech for project in Project.objects.filter(is_active=True) for tech in project.technologies_used}
        ),
        "status_options": [choice[0] for choice in Project.ProjectStatus.choices],
        "category_options": [choice[0] for choice in Project.ProjectCategory.choices],
        "filters": {
            "q": search,
            "technology": technology,
            "status": status,
            "category": category,
            "sort": sort,
        },
        "breadcrumbs": [{"label": "Projects", "url": ""}],
    }
    return render(request, "projects/projects_list.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project.objects.filter(is_active=True), slug=slug)
    ordered_ids = list(Project.objects.filter(is_active=True).order_by("order", "-start_date").values_list("id", flat=True))
    current_index = ordered_ids.index(project.id)
    previous_project = None
    next_project = None
    if current_index > 0:
        previous_project = Project.objects.get(id=ordered_ids[current_index - 1])
    if current_index < len(ordered_ids) - 1:
        next_project = Project.objects.get(id=ordered_ids[current_index + 1])

    related_projects = (
        Project.objects.filter(is_active=True, category=project.category)
        .exclude(pk=project.pk)
        .order_by("-is_featured", "order", "-start_date")[:3]
    )
    if not related_projects:
        related_projects = Project.objects.filter(is_active=True).exclude(pk=project.pk).order_by("order", "-start_date")[:3]

    context = {
        **base_page_context(
            "project_detail",
            f"{project.title} | Projects",
            project.description,
        ),
        "project": project,
        "project_gallery_images": project.gallery_images,
        "related_projects": related_projects,
        "previous_project": previous_project,
        "next_project": next_project,
        "breadcrumbs": [
            {"label": "Projects", "url": reverse("portfolio_app:projects")},
            {"label": project.title, "url": ""},
        ],
    }
    return render(request, "projects/project_detail.html", context)


def experience(request):
    context = {
        **base_page_context(
            "experience",
            "Work Experience",
            "Professional experience, responsibilities, and technical growth of Arjun Singh.",
        ),
        "experience_list": Experience.objects.filter(is_active=True).order_by("order", "-start_date"),
        "breadcrumbs": [{"label": "Experience", "url": ""}],
    }
    return render(request, "experience/experience.html", context)


def education(request):
    about_section = AboutSection.objects.filter(is_active=True).first()
    context = {
        **base_page_context(
            "education",
            "Education",
            "Academic background, CGPA, coursework, and technical foundation.",
        ),
        "education_list": Education.objects.filter(is_active=True).order_by("order", "-end_date"),
        "certification_list": Certification.objects.filter(is_active=True).order_by("order", "-issue_date"),
        "about": about_section,
        "breadcrumbs": [{"label": "Education", "url": ""}],
    }
    return render(request, "education/education.html", context)


def contact(request):
    if request.method == "POST":
        result = handle_contact_submission(request, "portfolio_app:contact")
        if not isinstance(result, ContactSubmissionForm):
            return result
        form = result
    else:
        form = ContactSubmissionForm()

    context = {
        **base_page_context(
            "contact",
            "Contact",
            "Get in touch with Arjun Singh for roles, collaborations, and technical discussions.",
        ),
        "contact_form": form,
        "contact_success_prompt": request.GET.get("submitted") == "1",
        "contact_info": ContactInformation.objects.filter(is_active=True).first(),
        "breadcrumbs": [{"label": "Contact", "url": ""}],
    }
    return render(request, "contact/contact.html", context)


def resume(request):
    contact_info = ContactInformation.objects.filter(is_active=True).first()
    context = {
        **base_page_context(
            "resume",
            "Resume",
            "Preview and download Arjun Singh's resume and profile summary.",
        ),
        "contact_info": contact_info,
        "about": AboutSection.objects.filter(is_active=True).first(),
        "breadcrumbs": [{"label": "Resume", "url": ""}],
    }
    return render(request, "resume/resume.html", context)


@require_GET
def filter_projects(request):
    projects = Project.objects.filter(is_active=True)
    technology = request.GET.get("technology", "").strip()
    status = request.GET.get("status", "").strip()
    category = request.GET.get("category", "").strip()
    search = request.GET.get("q", "").strip()

    if technology:
        projects = projects.filter(technologies_used__icontains=technology)
    if status:
        projects = projects.filter(status=status)
    if category:
        projects = projects.filter(category=category)
    if search:
        projects = projects.filter(Q(title__icontains=search) | Q(description__icontains=search))

    data = [
        {
            "title": project.title,
            "slug": project.slug,
            "description": project.description,
            "status": project.status,
            "category": project.category,
            "technologies": project.technologies_used,
            "url": project.get_absolute_url(),
        }
        for project in projects.order_by("order", "-is_featured", "-start_date")
    ]
    return JsonResponse({"results": data})


@require_GET
def search_skills(request):
    query = request.GET.get("q", "").strip()
    skills = TechnicalSkill.objects.filter(is_active=True)
    if query:
        skills = skills.filter(Q(skill_name__icontains=query) | Q(description__icontains=query))
    data = [
        {
            "name": skill.skill_name,
            "category": skill.category,
            "proficiency": skill.proficiency_level,
            "years": skill.years_of_experience,
        }
        for skill in skills.order_by("-proficiency_level", "skill_name")[:25]
    ]
    return JsonResponse({"results": data})


def page_not_found(request, exception=None):
    response = render(
        request,
        "errors/404.html",
        base_page_context(
            "404",
            "Page Not Found",
            "The page you were looking for could not be found.",
        ),
        status=404,
    )
    return response


def server_error(request):
    response = render(
        request,
        "errors/500.html",
        base_page_context(
            "500",
            "Server Error",
            "Something went wrong on the server.",
        ),
        status=500,
    )
    return response
