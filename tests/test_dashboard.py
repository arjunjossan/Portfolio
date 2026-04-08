from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from portfolio_app.models import SiteConfiguration, TechnicalSkill


class DashboardTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="staffuser",
            password="testpass123",
            is_staff=True,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("portfolio_app:dashboard_home"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_home_for_staff(self):
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(reverse("portfolio_app:dashboard_home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test_dashboard_can_create_singleton_content(self):
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.post(
            reverse("portfolio_app:dashboard_create", args=["site-configuration"]),
            {
                "site_name": "My Portfolio",
                "logo_text": "MP",
                "seo_title": "My Portfolio",
                "seo_description": "Portfolio description",
                "seo_keywords": "portfolio",
                "accent_text": "Developer portfolio",
                "availability_status": "Available",
                "footer_note": "Footer note",
                "resume_label": "Download CV",
                "show_theme_toggle": "on",
                "is_active": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SiteConfiguration.objects.count(), 1)

    def test_dashboard_can_create_skill(self):
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.post(
            reverse("portfolio_app:dashboard_create", args=["technical-skills"]),
            {
                "category": "Backend",
                "skill_name": "Django",
                "proficiency_level": 5,
                "icon": "fa-brands fa-python",
                "description": "Backend framework",
                "years_of_experience": 2,
                "is_active": "on",
                "order": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TechnicalSkill.objects.count(), 1)
