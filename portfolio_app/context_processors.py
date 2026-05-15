from types import SimpleNamespace
from urllib.parse import quote

from .models import ContactInformation, PageMetaData, SiteConfiguration, SocialMediaLink, WhatsAppWidget


def site_context(request):
    site_config = SiteConfiguration.objects.filter(is_active=True).first()
    global_contact = ContactInformation.objects.filter(is_active=True).first()
    whatsapp_widget = WhatsAppWidget.objects.filter(is_active=True).first()

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
        "whatsapp_widget": whatsapp_widget,
    }
