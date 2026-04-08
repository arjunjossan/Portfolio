from django.test import TestCase
from django.urls import reverse

from portfolio_app.models import Subscriber


class HomeViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("portfolio_app:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_contact_form_rejects_short_message(self):
        response = self.client.post(
            reverse("portfolio_app:contact"),
            {
                "name": "Arjun Singh",
                "email": "arjun@example.com",
                "subject": "Hello",
                "message": "Too short",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please share a bit more detail")

    def test_projects_page_loads(self):
        response = self.client.get(reverse("portfolio_app:projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/projects_list.html")

    def test_home_subscribe_form_creates_subscriber(self):
        response = self.client.post(
            reverse("portfolio_app:home"),
            {
                "form_type": "subscribe",
                "email": "subscriber@example.com",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subscriber.objects.filter(email="subscriber@example.com").exists())

    def test_home_subscribe_form_redirects_existing_subscriber_with_popup_state(self):
        Subscriber.objects.create(email="subscriber@example.com", is_active=True)

        response = self.client.post(
            reverse("portfolio_app:home"),
            {
                "form_type": "subscribe",
                "email": "subscriber@example.com",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("?subscription=already_subscribed", response.url)
