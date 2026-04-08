from datetime import date
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from portfolio_app.models import (
    AboutSection,
    Certification,
    ContactInformation,
    Education,
    Experience,
    HeroSection,
    Project,
    SiteConfiguration,
    SocialMediaLink,
    TechnicalSkill,
)


CV_PATH = Path("/Users/arjunsingh/Desktop/IDP /Applicant/Arjun CV.pdf")


class Command(BaseCommand):
    help = "Seed portfolio data using details extracted from Arjun CV.pdf."

    def handle(self, *args, **options):
        self.seed_site_configuration()
        self.seed_hero()
        self.seed_about()
        self.seed_skills()
        self.seed_projects()
        self.seed_experience()
        self.seed_education()
        self.seed_contact_information()
        self.seed_social_links()

        self.stdout.write(self.style.SUCCESS("Portfolio data seeded from CV details."))

    def seed_site_configuration(self):
        SiteConfiguration.objects.update_or_create(
            is_active=True,
            defaults={
                "site_name": "Arjun Singh",
                "logo_text": "AS",
                "seo_title": "Arjun Singh | Django Developer Portfolio",
                "seo_description": (
                    "Computer Science graduate with experience in Python, Django, "
                    "full-stack development, scalable web applications, and data-driven systems."
                ),
                "seo_keywords": (
                    "Arjun Singh, Django, Python, full-stack developer, portfolio, "
                    "data science, information technology"
                ),
                "accent_text": "Developer portfolio",
                "availability_status": "Open to roles, internships, and technical collaborations",
                "footer_note": "Built with Django to present projects, experience, and technical strengths with clarity.",
                "resume_label": "Download Resume",
                "show_theme_toggle": True,
            },
        )

    def seed_hero(self):
        HeroSection.objects.update_or_create(
            is_active=True,
            defaults={
                "title": "Hi, I'm Arjun Singh",
                "subtitle": (
                    "Computer Science graduate focused on Python, Django, scalable web systems, "
                    "and data-driven problem solving. I enjoy building reliable applications "
                    "that solve real business and user needs."
                ),
                "cta_button_text": "View My Work",
                "cta_button_url": "#projects",
                "secondary_button_text": "Get In Touch",
                "secondary_button_url": "#contact",
            },
        )

    def seed_about(self):
        AboutSection.objects.update_or_create(
            is_active=True,
            defaults={
                "title": "Building practical software with a product and systems mindset",
                "description": (
                    "I am a Computer Science graduate with hands-on experience in full-stack development, "
                    "backend systems, and technical operations. My recent work has centered on building "
                    "Django-powered applications, improving workflows, and translating real requirements "
                    "into maintainable software."
                ),
                "background_summary": (
                    "My academic and project work has strengthened my interest in backend engineering, "
                    "cloud-ready applications, and data-informed systems. I am focused on growing as a "
                    "developer by taking on meaningful technical challenges and building dependable software."
                ),
                "quick_facts": {
                    "projects_completed": "2+",
                    "years_in_tech": "4+",
                    "professional_roles": "2",
                    "cgpa": "7.6",
                },
                "masters_goals": (
                    "I want to keep deepening my understanding of scalable systems, data-driven applications, "
                    "and strong software engineering practice. My goal is to grow through hands-on work, "
                    "better system design, and consistent delivery of useful products."
                ),
            },
        )

    def seed_skills(self):
        skills = [
            ("Backend", "Python", 5, "fa-brands fa-python", 1),
            ("Backend", "Django", 5, "fa-solid fa-server", 2),
            ("Backend", "SQL", 4, "fa-solid fa-database", 3),
            ("Backend", "C++", 3, "fa-solid fa-code", 4),
            ("Frontend", "React", 4, "fa-brands fa-react", 5),
            ("Frontend", "WordPress", 3, "fa-brands fa-wordpress", 6),
            ("Tools", "Git", 4, "fa-brands fa-git-alt", 7),
            ("Tools", "Docker", 4, "fa-brands fa-docker", 8),
            ("Cloud", "Google Cloud Platform", 3, "fa-brands fa-google", 9),
            ("Tools", "VS Code", 5, "fa-solid fa-laptop-code", 10),
            ("Tools", "Visual Studio", 4, "fa-solid fa-code-branch", 11),
            ("Data Analysis", "Pandas", 4, "fa-solid fa-chart-line", 12),
            ("Data Analysis", "NumPy", 3, "fa-solid fa-calculator", 13),
            ("Data Analysis", "Matplotlib", 3, "fa-solid fa-chart-column", 14),
            ("Backend", "PostgreSQL", 4, "fa-solid fa-database", 15),
            ("Backend", "SQLite", 4, "fa-solid fa-database", 16),
        ]

        for category, name, proficiency, icon, order in skills:
            TechnicalSkill.objects.update_or_create(
                category=category,
                skill_name=name,
                defaults={
                    "proficiency_level": proficiency,
                    "icon": icon,
                    "description": f"Applied {name} in projects and practical portfolio work.",
                    "years_of_experience": 1 if name in {"Google Cloud Platform", "Matplotlib", "NumPy"} else 2,
                    "order": order,
                    "is_active": True,
                },
            )

    def seed_projects(self):
        projects = [
            {
                "title": "FitLance",
                "description": "A multi-tenant gym management SaaS for platform owners, gym owners, trainers, and clients with secure role-based dashboards and progress tracking.",
                "technologies_used": [
                    "React",
                    "TypeScript",
                    "Supabase",
                    "PostgreSQL",
                    "Tailwind CSS",
                    "shadcn/ui",
                    "Framer Motion",
                    "Recharts",
                ],
                "project_url": "https://fitlance.lovable.app",
                "github_url": "",
                "start_date": date(2026, 1, 1),
                "end_date": None,
                "is_featured": True,
                "status": Project.ProjectStatus.COMPLETED,
                "category": Project.ProjectCategory.FULL_STACK,
                "detailed_description": (
                    "Built FitLance as a full-stack SaaS platform for gym operations, designed around four distinct "
                    "user roles: platform owners, gym owners, trainers, and clients. The product combines workout and "
                    "diet plan assignment, attendance, hydration tracking, progress analytics, and leaderboard features "
                    "inside one role-based application. The backend uses Supabase with PostgreSQL Row-Level Security, "
                    "RBAC through dedicated role tables and helper functions, and secure admin workflows through edge "
                    "functions for privileged operations."
                ),
                "key_features": [
                    "Multi-tenant SaaS architecture with role-based dashboards for platform owners, gym owners, trainers, and clients",
                    "Secure access control using PostgreSQL Row-Level Security, RBAC, and protected admin operations",
                    "Workout and diet planning with per-exercise and per-meal progress tracking",
                    "Hydration logging, attendance tracking, leaderboard logic, and chart-based progress analytics",
                    "Subscription-ready structure for gym plans, limits, and platform-scale growth",
                ],
                "lessons_learned": (
                    "This project deepened my understanding of SaaS product design, secure multi-tenant data access, "
                    "role-aware UX, and the difference between scaffolding quickly and building reliable business logic. "
                    "It also reinforced how important database design and authorization boundaries are in full-stack applications."
                ),
                "order": 1,
            },
            {
                "title": "Sweetora",
                "description": "A premium gifting e-commerce platform with personalized checkout, phone-based authentication, admin commerce tooling, and production-grade email workflows.",
                "technologies_used": [
                    "React",
                    "TypeScript",
                    "Supabase",
                    "PostgreSQL",
                    "Tailwind CSS",
                    "TanStack Query",
                    "Resend",
                    "Deno Edge Functions",
                ],
                "project_url": "https://sweetorashop.lovable.app",
                "github_url": "",
                "start_date": date(2025, 12, 1),
                "end_date": None,
                "is_featured": True,
                "status": Project.ProjectStatus.COMPLETED,
                "category": Project.ProjectCategory.FULL_STACK,
                "detailed_description": (
                    "Built Sweetora as a full-stack gifting commerce platform focused on a more personalized buying experience. "
                    "The app combines curated product discovery, custom gifting options like love messages, scheduled delivery, "
                    "and premium gift wrapping, along with a mobile-friendly storefront, multi-step checkout, and a full admin "
                    "dashboard for product, order, category, and shop settings management. On the backend, it uses Supabase with "
                    "PostgreSQL Row-Level Security, RBAC, edge functions, and a Resend-powered email system for transactional "
                    "updates, marketing campaigns, unsubscribe flows, and send queue processing."
                ),
                "key_features": [
                    "Personalized gifting flow with love messages, scheduled delivery dates, premium gift wrap, and dynamic price breakdowns",
                    "Multi-step checkout with guest-to-user conversion through phone-based authentication alongside email and Google sign-in",
                    "Admin dashboard for product CRUD, category management, order tracking, pricing settings, and subscriber operations",
                    "Production-grade email infrastructure with transactional templates, campaign sending, suppression handling, and unsubscribe flows",
                    "Secure commerce architecture using PostgreSQL RLS, RBAC, and server-side admin verification in edge functions",
                ],
                "lessons_learned": (
                    "Sweetora strengthened my understanding of end-to-end commerce workflows, especially how product modeling, checkout "
                    "state, authentication, and customer communication all connect. It also pushed me to think more deeply about email "
                    "delivery reliability, admin tooling, and how to build polished business features on top of secure backend foundations."
                ),
                "order": 2,
            },
            {
                "title": "Drop",
                "description": "A premium hydration and habit tracking app with gamification, smart reminders, weekly analytics, and a high-fidelity Flutter interface.",
                "technologies_used": [
                    "Flutter",
                    "Dart",
                    "Riverpod",
                    "Firebase Auth",
                    "Cloud Firestore",
                    "Firebase Storage",
                    "Shared Preferences",
                    "fl_chart",
                ],
                "project_url": "",
                "github_url": "",
                "start_date": date(2025, 10, 1),
                "end_date": None,
                "is_featured": True,
                "status": Project.ProjectStatus.COMPLETED,
                "category": Project.ProjectCategory.FULL_STACK,
                "detailed_description": (
                    "Built Drop as a cross-platform hydration and habit tracking app focused on making daily health routines "
                    "feel rewarding instead of repetitive. The app lets users log water intake against customizable daily goals, "
                    "review weekly progress trends, manage profile data, and stay engaged through streaks, XP progression, "
                    "unlockable badges, confetti celebrations, and contextual reminder notifications. It was created with "
                    "Antigravity-assisted generation as part of the workflow, and I’m presenting it honestly as an AI-assisted app "
                    "rather than pretending every part was hand-coded from zero. The product stack centers on Flutter with Riverpod "
                    "for predictable state management, Firebase Authentication and Firestore for secure cloud sync, Firebase Storage "
                    "for profile assets, and polished UI work using custom liquid-style animations, Material 3, and chart-driven analytics."
                ),
                "key_features": [
                    "Hydration logging with custom daily goals, quantity tracking, timestamps, and visual progress feedback",
                    "Gamification system with streaks, XP progression, levels, and unlockable badges to encourage daily consistency",
                    "Context-aware local notifications that adapt to progress, time of day, and goal completion state",
                    "Weekly analytics dashboards powered by chart visualization to help users understand hydration patterns",
                    "Premium Flutter UI with dark mode, glassmorphism styling, smooth transitions, and liquid-inspired micro-interactions",
                ],
                "lessons_learned": (
                    "Drop reinforced the importance of being honest about AI-assisted development while still being clear about the value of "
                    "product thinking, customization, UX decisions, and integration work. It also helped me better understand how to combine "
                    "Flutter state management, Firebase services, local notifications, and polished motion design into a cohesive mobile experience."
                ),
                "order": 3,
            },
            {
                "title": "Company Website",
                "description": "A Django and React based company platform that improved digital presence and inquiry management.",
                "technologies_used": ["Python", "Django", "React", "PostgreSQL"],
                "start_date": date(2025, 5, 1),
                "end_date": date(2025, 8, 1),
                "is_featured": True,
                "status": Project.ProjectStatus.COMPLETED,
                "category": Project.ProjectCategory.FULL_STACK,
                "detailed_description": (
                    "Developed a full-stack company website using Django and React to improve digital presence, "
                    "centralize service information, and streamline inquiry handling. The project included an admin-focused "
                    "workflow with optimized backend performance and secure database handling."
                ),
                "key_features": [
                    "Admin dashboard to manage client inquiries and services efficiently",
                    "Responsive full-stack interface built with Django and React",
                    "Optimized backend performance with secure PostgreSQL integration",
                ],
                "lessons_learned": (
                    "This project strengthened my understanding of full-stack architecture, deployment readiness, "
                    "admin workflow design, and the tradeoffs involved in building maintainable business applications."
                ),
                "order": 4,
            },
            {
                "title": "Student Performance Analysis System",
                "description": "A data analysis project using Pandas and Matplotlib to uncover student performance trends.",
                "technologies_used": ["Pandas", "NumPy", "Matplotlib"],
                "start_date": date(2025, 11, 1),
                "end_date": date(2026, 1, 1),
                "is_featured": True,
                "status": Project.ProjectStatus.COMPLETED,
                "category": Project.ProjectCategory.DATA,
                "detailed_description": (
                    "Performed cleaning, preprocessing, and exploratory data analysis on student performance data "
                    "to identify trends and generate subject-wise insights. Built visual summaries using Matplotlib "
                    "to make patterns easier to interpret and communicate."
                ),
                "key_features": [
                    "Data cleaning and preprocessing pipeline using Pandas and NumPy",
                    "Exploratory analysis for subject-wise performance trends",
                    "Visualization dashboards using Matplotlib for decision-friendly insights",
                ],
                "lessons_learned": (
                    "The project improved my confidence in structured analysis, communicating results visually, "
                    "and connecting raw data work to actionable insights."
                ),
                "order": 5,
            },
        ]

        for project in projects:
            Project.objects.update_or_create(
                title=project["title"],
                defaults={**project, "is_active": True},
            )

    def seed_experience(self):
        experiences = [
            {
                "job_title": "IT Supervisor",
                "company_name": "Five Nine Consultancies Pvt. Ltd.",
                "location": "Bareilly, Uttar Pradesh",
                "start_date": date(2025, 3, 1),
                "end_date": None,
                "is_current": True,
                "description": (
                    "Working across website delivery, backend logic, hosting, debugging, and performance optimization "
                    "to improve the company's digital workflow and service presence."
                ),
                "key_responsibilities": [
                    "Developed and deployed a company website serving 100+ users",
                    "Built modules for client inquiries, services, and admin panel management",
                    "Managed hosting, backend logic, debugging, and performance optimization",
                ],
                "technologies_used": ["Django", "Python", "PostgreSQL", "Hosting", "Admin Systems"],
                "order": 1,
            },
            {
                "job_title": "Immigration Documentation Intern",
                "company_name": "Passion Trip Planner",
                "location": "Paliya, Uttar Pradesh",
                "start_date": date(2024, 7, 1),
                "end_date": date(2025, 2, 1),
                "is_current": False,
                "description": (
                    "Supported documentation operations and digital workflow improvements while assisting clients "
                    "with submission-related queries."
                ),
                "key_responsibilities": [
                    "Managed digital records and supported transition to digital workflows",
                    "Prepared documentation using Excel, Word, and Canva",
                    "Assisted clients with technical queries during application submissions",
                ],
                "technologies_used": ["Excel", "Word", "Canva", "Digital Records"],
                "order": 2,
            },
        ]

        for experience in experiences:
            Experience.objects.update_or_create(
                job_title=experience["job_title"],
                company_name=experience["company_name"],
                defaults={**experience, "is_active": True},
            )

    def seed_education(self):
        education_entries = [
            {
                "degree_name": "B.Tech",
                "institution_name": "Lovely Professional University",
                "location": "Punjab, India",
                "field_of_study": "Computer Science",
                "start_date": date(2020, 8, 1),
                "end_date": date(2024, 5, 1),
                "gpa_cgpa": "CGPA: 7.6",
                "highlights": [
                    "Completed undergraduate studies in Computer Science",
                    "Built a foundation in software development and backend systems",
                    "Strengthened interest in scalable applications and data-driven technologies",
                ],
                "relevant_coursework": ["Data Structures", "OOP", "Web Development", "Database Systems"],
                "order": 1,
            },
            {
                "degree_name": "12th Standard",
                "institution_name": "Guru Teg Bahadur Educational Academy",
                "location": "Shahjahanpur, Uttar Pradesh",
                "field_of_study": "Science (Non-Medical)",
                "start_date": date(2019, 4, 1),
                "end_date": date(2020, 3, 1),
                "gpa_cgpa": "Percentage: 68",
                "highlights": [
                    "Completed higher secondary studies in science",
                    "Built early grounding in analytical and technical subjects",
                ],
                "relevant_coursework": ["Physics", "Mathematics", "Computer Fundamentals"],
                "order": 2,
            },
        ]

        for education in education_entries:
            Education.objects.update_or_create(
                degree_name=education["degree_name"],
                institution_name=education["institution_name"],
                defaults={**education, "is_active": True},
            )

    def seed_contact_information(self):
        contact, _ = ContactInformation.objects.update_or_create(
            email="arjunsinghjossan@gmail.com",
            defaults={
                "phone": "+91 8737067071",
                "location": "Punjab / Uttar Pradesh, India",
                "cv_download_enabled": True,
                "is_active": True,
            },
        )

        if CV_PATH.exists() and not contact.resume_pdf:
            with CV_PATH.open("rb") as cv_file:
                contact.resume_pdf.save("Arjun-Singh-CV.pdf", File(cv_file), save=True)

    def seed_social_links(self):
        links = [
            ("LinkedIn", "https://linkedin.com/in/arjunsinghjossan", "fa-brands fa-linkedin-in", 1),
            ("GitHub", "https://github.com/arjunjossan", "fa-brands fa-github", 2),
            ("Email", "mailto:arjunsinghjossan@gmail.com", "fa-solid fa-envelope", 3),
        ]

        for platform, profile_url, icon_code, order in links:
            SocialMediaLink.objects.update_or_create(
                platform=platform,
                defaults={
                    "profile_url": profile_url,
                    "icon_code": icon_code,
                    "order": order,
                    "is_active": True,
                },
            )
