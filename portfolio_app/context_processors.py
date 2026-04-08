from types import SimpleNamespace

from .models import ContactInformation, PageMetaData, SiteConfiguration, SocialMediaLink


def site_context(request):
    site_config = SiteConfiguration.objects.filter(is_active=True).first()
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
        "global_contact": ContactInformation.objects.filter(is_active=True).first(),
        "global_social_links": SocialMediaLink.objects.filter(is_active=True).order_by("order", "platform"),
        "global_page_meta": {item.page_name: item for item in PageMetaData.objects.all()},
    }
