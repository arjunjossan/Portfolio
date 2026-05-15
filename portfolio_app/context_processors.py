from types import SimpleNamespace
from urllib.parse import quote

from .models import ContactInformation, PageMetaData, SiteConfiguration, SocialMediaLink, WhatsAppWidget


def site_context(request):
    site_config = SiteConfiguration.objects.filter(is_active=True).first()
    global_contact = ContactInformation.objects.filter(is_active=True).first()
    whatsapp_widget = WhatsAppWidget.objects.filter(is_active=True).first()
    popup_subscription_status = request.GET.get("popup_subscription", "").strip()
    popup_feedback_prompt = None

    if popup_subscription_status:
        popup_prompt_map = {
            "subscribed": {
                "status": "subscribed",
                "theme": "success",
                "eyebrow": "Saved Successfully",
                "title": "You are on the update list now.",
                "copy": "Thanks for sharing your details. I will send meaningful portfolio launches, case studies, and major updates here.",
                "icon": "fa-solid fa-check",
            },
            "reactivated": {
                "status": "reactivated",
                "theme": "success",
                "eyebrow": "Subscription Restored",
                "title": "Your updates are active again.",
                "copy": "Welcome back. This email will receive future portfolio releases and important project announcements.",
                "icon": "fa-solid fa-rotate-right",
            },
            "already_subscribed": {
                "status": "already_subscribed",
                "theme": "info",
                "eyebrow": "Already Subscribed",
                "title": "This email is already registered.",
                "copy": "You are already in the portfolio updates circle, so there is nothing else you need to do.",
                "icon": "fa-solid fa-bell",
            },
            "invalid": {
                "status": "invalid",
                "theme": "error",
                "eyebrow": "Submission Incomplete",
                "title": "Please enter a valid name and Gmail address.",
                "copy": "Your details were not saved this time. Review the form and try again with complete information.",
                "icon": "fa-solid fa-triangle-exclamation",
            },
        }
        prompt_config = popup_prompt_map.get(popup_subscription_status)
        if prompt_config:
            popup_feedback_prompt = SimpleNamespace(**prompt_config)

    if whatsapp_widget is None:
        fallback_phone_number = ""
        if global_contact and global_contact.phone:
            fallback_phone_number = "".join(character for character in global_contact.phone if character.isdigit())

        fallback_message = "Hello, I came across your portfolio and would like to connect."
        whatsapp_widget = SimpleNamespace(
            label="WhatsApp",
            title="Start a conversation",
            subtitle="Usually replies within a few hours",
            description="Share your project, question, or collaboration idea and continue the conversation on WhatsApp.",
            phone_number=fallback_phone_number,
            prefilled_message=fallback_message,
            button_text="Open WhatsApp",
            is_active=bool(fallback_phone_number),
            whatsapp_url=(
                f"https://wa.me/{fallback_phone_number}?text={quote(fallback_message)}"
                if fallback_phone_number
                else ""
            ),
        )

    if site_config is None:
        site_config = SimpleNamespace(
            site_name="Portfolio",
            logo_text="AS",
            seo_title="Professional Portfolio",
            seo_description="A professional Django portfolio website ready for dynamic admin-managed content.",
            seo_keywords="portfolio,django,developer",
            accent_text="Developer portfolio",
            availability_status="Available for professional opportunities and collaborations",
            footer_note="Update this shared site content from the Django admin panel.",
            resume_label="Download CV",
            show_theme_toggle=True,
        )

    return {
        "site_config": site_config,
        "global_contact": global_contact,
        "global_social_links": SocialMediaLink.objects.filter(is_active=True).order_by("order", "platform"),
        "global_page_meta": {item.page_name: item for item in PageMetaData.objects.all()},
        "popup_feedback_prompt": popup_feedback_prompt,
        "whatsapp_widget": whatsapp_widget,
    }
