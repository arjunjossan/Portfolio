from urllib.parse import quote, urlparse

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from .models import EmailCampaign, EmailDelivery


def site_name():
    return getattr(settings, "SITE_NAME", "") or "Portfolio Updates"


def _absolute_url(request, path_or_url):
    if not path_or_url:
        return ""
    parsed = urlparse(path_or_url)
    if parsed.scheme and parsed.netloc:
        return path_or_url
    if request is None:
        base_url = getattr(settings, "SITE_URL", "").rstrip("/")
        if base_url and path_or_url.startswith("/"):
            return f"{base_url}{path_or_url}"
        return path_or_url
    return request.build_absolute_uri(path_or_url)


def campaign_projects(campaign):
    return campaign.get_featured_projects()


def campaign_context(campaign, request=None, delivery=None):
    unsubscribe_url = ""
    tracking_pixel_url = ""
    if delivery and delivery.subscriber:
        unsubscribe_url = _absolute_url(request, delivery.subscriber.unsubscribe_path())
    if delivery and campaign.track_opens:
        tracking_pixel_url = _absolute_url(
            request,
            reverse("portfolio_app:email_open_tracking", args=[delivery.token]),
        )

    return {
        "campaign": campaign,
        "site_name": site_name(),
        "featured_projects": campaign_projects(campaign),
        "unsubscribe_url": unsubscribe_url,
        "tracking_pixel_url": tracking_pixel_url,
    }


def tracked_url(request, delivery, target_url):
    if not target_url:
        return ""
    if not delivery or not delivery.campaign.track_clicks:
        return _absolute_url(request, target_url)
    path = reverse("portfolio_app:email_click_tracking", args=[delivery.token])
    if request is None:
        return f"{path}?target={quote(target_url, safe='')}"
    return request.build_absolute_uri(f"{path}?target={quote(target_url, safe='')}")


def build_campaign_email(campaign, request=None, delivery=None):
    context = campaign_context(campaign, request=request, delivery=delivery)
    context["cta_url"] = tracked_url(request, delivery, campaign.cta_url)
    context["featured_project_cards"] = [
        {
            "project": project,
            "url": tracked_url(request, delivery, project.get_absolute_url()),
        }
        for project in context["featured_projects"]
    ]
    html_body = render_to_string("emails/campaign_email.html", context)
    text_body = render_to_string("emails/campaign_email.txt", context)
    return text_body, html_body


def sync_campaign_metrics(campaign):
    deliveries = campaign.deliveries.all()
    sent_deliveries = deliveries.filter(status=EmailDelivery.DeliveryStatus.SENT)
    sent_recipients = sent_deliveries.count()
    open_count = sent_deliveries.filter(open_count__gt=0).count()
    click_count = sent_deliveries.filter(click_count__gt=0).count()
    campaign.recipient_count = sent_recipients
    campaign.open_count = open_count
    campaign.click_count = click_count
    campaign.save(update_fields=["recipient_count", "open_count", "click_count", "updated_at"])


def send_test_campaign(campaign, recipient_emails, request=None):
    recipients = [email.strip().lower() for email in recipient_emails if email and email.strip()]
    if not recipients:
        return 0

    connection = get_connection(fail_silently=False)
    messages = []
    for recipient in recipients:
        delivery, _ = EmailDelivery.objects.update_or_create(
            campaign=campaign,
            email=recipient,
            defaults={
                "status": EmailDelivery.DeliveryStatus.TEST,
                "subject_snapshot": campaign.subject,
                "sent_at": timezone.now(),
                "error_message": "",
            },
        )
        text_body, html_body = build_campaign_email(campaign, request=request, delivery=delivery)
        message = EmailMultiAlternatives(
            subject=f"[Test] {campaign.subject}",
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            connection=connection,
        )
        message.attach_alternative(html_body, "text/html")
        messages.append(message)

    connection.send_messages(messages)
    return len(messages)


def send_campaign(campaign, request=None):
    subscribers = list(campaign.get_target_subscribers())
    if not subscribers:
        return 0

    campaign.status = EmailCampaign.CampaignStatus.SENDING
    campaign.sending_started_at = timezone.now()
    campaign.last_error = ""
    campaign.save(update_fields=["status", "sending_started_at", "last_error", "updated_at"])

    connection = get_connection(fail_silently=False)
    messages = []
    deliveries = []
    now = timezone.now()

    for subscriber in subscribers:
        delivery, _ = EmailDelivery.objects.update_or_create(
            campaign=campaign,
            email=subscriber.email,
            defaults={
                "subscriber": subscriber,
                "status": EmailDelivery.DeliveryStatus.SENT,
                "subject_snapshot": campaign.subject,
                "sent_at": now,
                "error_message": "",
            },
        )
        text_body, html_body = build_campaign_email(campaign, request=request, delivery=delivery)
        message = EmailMultiAlternatives(
            subject=campaign.subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
            connection=connection,
        )
        message.attach_alternative(html_body, "text/html")
        messages.append(message)
        deliveries.append(delivery)

    try:
        connection.send_messages(messages)
    except Exception as exc:
        campaign.status = EmailCampaign.CampaignStatus.FAILED
        campaign.last_error = str(exc)
        campaign.save(update_fields=["status", "last_error", "updated_at"])
        raise

    campaign.status = EmailCampaign.CampaignStatus.SENT
    campaign.sent_at = timezone.now()
    campaign.last_error = ""
    campaign.recipient_count = len(deliveries)
    campaign.save(update_fields=["status", "sent_at", "last_error", "recipient_count", "updated_at"])
    sync_campaign_metrics(campaign)
    return len(deliveries)
