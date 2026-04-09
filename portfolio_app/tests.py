from datetime import date
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from portfolio_app.email_marketing import send_campaign
from portfolio_app.models import EmailCampaign, EmailDelivery, Project, Subscriber
from portfolio_app.views import email_click_tracking, email_open_tracking


class EmailMarketingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.project = Project.objects.create(
            title="Portfolio Launch",
            description="A full redesign of the portfolio experience.",
            technologies_used=["Django", "Tailwind"],
            start_date=date(2026, 4, 1),
            status=Project.ProjectStatus.COMPLETED,
            detailed_description="Launch details",
        )
        self.subscriber = Subscriber.objects.create(email="reader@example.com")
        self.campaign = EmailCampaign.objects.create(
            title="April Portfolio Update",
            subject="New portfolio projects are live",
            headline="Fresh work is now live",
            intro="A quick update from the portfolio studio.",
            content="I just published a new set of project case studies.",
            cta_label="Visit the portfolio",
            cta_url="https://example.com/portfolio",
        )
        self.campaign.featured_projects.add(self.project)

    @patch("portfolio_app.email_marketing.get_connection")
    def test_send_campaign_creates_delivery_and_marks_campaign_sent(self, mock_get_connection):
        connection = mock_get_connection.return_value
        connection.send_messages.return_value = 1

        sent_count = send_campaign(self.campaign)

        self.assertEqual(sent_count, 1)
        self.campaign.refresh_from_db()
        delivery = EmailDelivery.objects.get(campaign=self.campaign, email=self.subscriber.email)
        self.assertEqual(self.campaign.status, EmailCampaign.CampaignStatus.SENT)
        self.assertEqual(self.campaign.recipient_count, 1)
        self.assertEqual(delivery.status, EmailDelivery.DeliveryStatus.SENT)
        self.assertTrue(delivery.sent_at)

    def test_open_and_click_tracking_update_delivery_metrics(self):
        delivery = EmailDelivery.objects.create(
            campaign=self.campaign,
            subscriber=self.subscriber,
            email=self.subscriber.email,
            status=EmailDelivery.DeliveryStatus.SENT,
        )

        open_response = email_open_tracking(self.factory.get("/email/open/"), delivery.token)
        click_response = email_click_tracking(
            self.factory.get("/email/click/", {"target": "https://example.com/project"}),
            delivery.token,
        )

        delivery.refresh_from_db()
        self.campaign.refresh_from_db()
        self.assertEqual(open_response.status_code, 200)
        self.assertEqual(click_response.status_code, 302)
        self.assertEqual(delivery.open_count, 1)
        self.assertEqual(delivery.click_count, 1)
        self.assertEqual(self.campaign.open_count, 1)
        self.assertEqual(self.campaign.click_count, 1)
