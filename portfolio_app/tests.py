from datetime import date
from pathlib import Path
from unittest.mock import patch

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from portfolio_app.models import ContactSubmission, HeroSection, Project, Subscriber


class ProjectModelTests(TestCase):
    def test_slug_is_generated_for_project(self):
        project = Project.objects.create(
            title="Admissions Dashboard",
            description="Short summary",
            technologies_used=["Django"],
            start_date=date(2025, 1, 1),
            status=Project.ProjectStatus.COMPLETED,
            detailed_description="Detailed description for the project.",
        )

        self.assertEqual(project.slug, "admissions-dashboard")

    def test_duplicate_titles_receive_unique_slugs(self):
        base_data = {
            "title": "Research Portal",
            "description": "Summary",
            "technologies_used": ["Django"],
            "start_date": date(2025, 1, 1),
            "status": Project.ProjectStatus.COMPLETED,
            "detailed_description": "Details",
        }
        first = Project.objects.create(**base_data)
        second = Project.objects.create(**base_data)

        self.assertEqual(first.slug, "research-portal")
        self.assertEqual(second.slug, "research-portal-2")


class ContactSubmissionTests(TestCase):
    def test_submission_defaults_to_unread(self):
        submission = ContactSubmission.objects.create(
            name="Arjun Singh",
            email="arjun@example.com",
            subject="Graduate collaboration",
            message="I would like to discuss a graduate opportunity in detail.",
        )

        self.assertFalse(submission.is_read)
        self.assertFalse(submission.response_sent)


class HeroSectionTests(TestCase):
    @patch("portfolio_app.models.subprocess.run")
    def test_headline_image_converts_heic_uploads_to_jpg(self, mock_run):
        def fake_sips(command, check, capture_output):
            output_path = command[-1]
            Path(output_path).write_bytes(b"jpeg-bytes")

        mock_run.side_effect = fake_sips

        hero = HeroSection.objects.create(
            title="Hero",
            subtitle="Subtitle",
            cta_button_text="Explore",
            cta_button_url="#projects",
            headline_image=SimpleUploadedFile("portrait.heic", b"heic-bytes", content_type="image/heic"),
        )

        self.assertTrue(hero.headline_image.name.endswith(".jpg"))
        mock_run.assert_called_once()


class SubscriberTests(TestCase):
    def test_subscriber_defaults_to_active(self):
        subscriber = Subscriber.objects.create(email="updates@example.com")
        self.assertTrue(subscriber.is_active)

    def test_popup_subscription_stores_name_and_email(self):
        response = self.client.post(
            reverse("portfolio_app:subscribe_popup"),
            {
                "name": "Arjun Singh",
                "email": "arjun242042@gmail.com",
                "next": reverse("portfolio_app:home"),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("popup_subscription=subscribed", response.url)
        subscriber = Subscriber.objects.get(email="arjun242042@gmail.com")
        self.assertEqual(subscriber.name, "Arjun Singh")
