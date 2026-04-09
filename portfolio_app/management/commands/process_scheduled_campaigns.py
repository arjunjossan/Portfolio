from django.core.management.base import BaseCommand
from django.utils import timezone

from portfolio_app.email_marketing import send_campaign
from portfolio_app.models import EmailCampaign


class Command(BaseCommand):
    help = "Send email campaigns that are scheduled and due."

    def handle(self, *args, **options):
        now = timezone.now()
        campaigns = EmailCampaign.objects.filter(
            status=EmailCampaign.CampaignStatus.SCHEDULED,
            scheduled_for__isnull=False,
            scheduled_for__lte=now,
        ).order_by("scheduled_for")

        if not campaigns.exists():
            self.stdout.write(self.style.NOTICE("No scheduled campaigns are due right now."))
            return

        for campaign in campaigns:
            count = send_campaign(campaign)
            self.stdout.write(self.style.SUCCESS(f"Sent '{campaign.title}' to {count} subscribers."))
