from django.contrib import admin, messages
from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

from .email_marketing import build_campaign_email, send_campaign, send_test_campaign
from .forms import EmailCampaignDashboardForm
from .models import (
    AboutSection,
    Certification,
    ContactInformation,
    ContactSubmission,
    EmailCampaign,
    EmailDelivery,
    Education,
    Experience,
    HeroSection,
    PageMetaData,
    Project,
    ProjectDetailImage,
    SiteConfiguration,
    SocialMediaLink,
    Subscriber,
    TechnicalSkill,
)


admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Content Management Dashboard"


class HeroSectionAdminForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = "__all__"
        widgets = {
            "headline_image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*,.heic,.heif,.avif,.svg,.bmp,.tif,.tiff,.webp",
                }
            )
        }


class EmailDeliveryInline(admin.TabularInline):
    model = EmailDelivery
    extra = 0
    can_delete = False
    fields = ("email", "status", "sent_at", "opened_at", "clicked_at", "open_count", "click_count", "error_message")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False


class ProjectDetailImageInline(admin.StackedInline):
    model = ProjectDetailImage
    extra = 1
    fields = ("image", "alt_text", "order", "is_active")


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonAdmin):
    list_display = ("site_name", "availability_status", "show_theme_toggle", "is_active")


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    form = HeroSectionAdminForm
    list_display = ("title", "cover_style", "is_active")
    fieldsets = (
        (
            "Main content",
            {
                "fields": (
                    "title",
                    "subtitle",
                    "headline_image",
                )
            },
        ),
        (
            "Image cover text",
            {
                "description": "These fields control the magazine-style text shown on top of the hero image.",
                "fields": (
                    "cover_label",
                    "cover_heading",
                    "cover_caption",
                    "cover_style",
                    "cover_label_font",
                    "cover_heading_font",
                    "cover_caption_font",
                    "cover_text_opacity",
                    "cover_heading_offset_x",
                    "cover_heading_offset_y",
                ),
            },
        ),
        ("Settings", {"fields": ("is_active",)}),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    list_display = ("title", "is_active")


@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ("skill_name", "category", "proficiency_level", "years_of_experience", "order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("skill_name",)
    ordering = ("category", "order", "skill_name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "is_featured", "order", "preview_link", "is_active")
    list_filter = ("category", "status", "is_featured", "is_active")
    list_editable = ("is_featured", "order", "is_active")
    search_fields = ("title", "description", "detailed_description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectDetailImageInline]

    @admin.display(description="Preview")
    def preview_link(self, obj):
        if not obj.slug:
            return "-"
        return format_html('<a href="{}" target="_blank">Open</a>', obj.get_absolute_url())


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("job_title", "company_name", "is_current", "start_date", "end_date", "order", "is_active")
    list_filter = ("is_current", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("job_title", "company_name", "location")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree_name", "institution_name", "gpa_cgpa", "end_date", "order", "is_active")
    list_filter = ("is_active",)
    list_editable = ("order", "is_active")
    search_fields = ("degree_name", "institution_name", "field_of_study")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issue_date", "order", "is_active")
    list_filter = ("is_active",)
    list_editable = ("order", "is_active")
    search_fields = ("title", "issuer")


@admin.register(ContactInformation)
class ContactInformationAdmin(SingletonAdmin):
    list_display = ("email", "phone", "location", "cv_download_enabled", "is_active")


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "profile_url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("platform",)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message_type", "subject", "submitted_at", "is_read", "response_sent")
    list_filter = ("message_type", "is_read", "response_sent", "submitted_at")
    search_fields = ("name", "email", "company", "subject", "message")
    readonly_fields = ("name", "email", "phone", "company", "message_type", "subject", "message", "attachment", "submitted_at")

    def has_add_permission(self, request):
        return False


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "subscribed_at", "unsubscribed_at")
    list_filter = ("is_active", "subscribed_at", "unsubscribed_at")
    search_fields = ("email",)
    list_editable = ("is_active",)
    readonly_fields = ("unsubscribe_token", "unsubscribed_at")

    def has_add_permission(self, request):
        return False


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    form = EmailCampaignDashboardForm
    change_form_template = "admin/portfolio_app/emailcampaign/change_form.html"
    inlines = [EmailDeliveryInline]
    list_display = (
        "title",
        "campaign_type",
        "status_badge",
        "audience",
        "scheduled_for",
        "recipient_count",
        "open_rate_display",
        "click_rate_display",
        "sent_at",
    )
    list_filter = ("campaign_type", "status", "audience", "template_style", "track_opens", "track_clicks")
    search_fields = ("title", "subject", "headline", "content")
    filter_horizontal = ("featured_projects",)
    readonly_fields = (
        "status",
        "created_by",
        "sending_started_at",
        "sent_at",
        "recipient_count",
        "open_count",
        "click_count",
        "last_error",
        "performance_summary",
        "preview_link",
        "send_test_link",
        "send_now_link",
    )
    fieldsets = (
        (
            "Campaign planning",
            {
                "fields": (
                    "title",
                    "campaign_type",
                    "audience",
                    "subject",
                    "preview_text",
                    "template_style",
                    "internal_notes",
                    "created_by",
                )
            },
        ),
        (
            "Email content",
            {
                "fields": (
                    "headline",
                    "intro",
                    "content",
                    ("cta_label", "cta_url"),
                    "featured_projects",
                    ("include_latest_projects", "latest_projects_count"),
                )
            },
        ),
        (
            "Delivery controls",
            {
                "fields": (
                    ("track_opens", "track_clicks"),
                    "scheduled_for",
                    "test_recipients",
                    "status",
                    "sending_started_at",
                    "sent_at",
                    "last_error",
                )
            },
        ),
        (
            "Performance",
            {
                "fields": (
                    "recipient_count",
                    "open_count",
                    "click_count",
                    "performance_summary",
                    "preview_link",
                    "send_test_link",
                    "send_now_link",
                )
            },
        ),
    )
    actions = ("send_selected_campaigns", "duplicate_selected_campaigns")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:campaign_id>/preview/",
                self.admin_site.admin_view(self.preview_view),
                name="portfolio_app_emailcampaign_preview",
            ),
            path(
                "<int:campaign_id>/send-test/",
                self.admin_site.admin_view(self.send_test_view),
                name="portfolio_app_emailcampaign_send_test",
            ),
            path(
                "<int:campaign_id>/send-now/",
                self.admin_site.admin_view(self.send_now_view),
                name="portfolio_app_emailcampaign_send_now",
            ),
        ]
        return custom_urls + urls

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {
            EmailCampaign.CampaignStatus.DRAFT: "#475569",
            EmailCampaign.CampaignStatus.SCHEDULED: "#2563eb",
            EmailCampaign.CampaignStatus.SENDING: "#f59e0b",
            EmailCampaign.CampaignStatus.SENT: "#059669",
            EmailCampaign.CampaignStatus.FAILED: "#dc2626",
        }
        color = colors.get(obj.status, "#475569")
        return format_html(
            '<span style="display:inline-flex;padding:4px 10px;border-radius:999px;background:{}15;color:{};font-weight:700;">{}</span>',
            color,
            color,
            obj.get_status_display(),
        )

    @admin.display(description="Open rate")
    def open_rate_display(self, obj):
        return f"{obj.open_rate}%"

    @admin.display(description="Click rate")
    def click_rate_display(self, obj):
        return f"{obj.click_rate}%"

    @admin.display(description="Performance summary")
    def performance_summary(self, obj):
        return f"Sent: {obj.recipient_count} | Opens: {obj.open_count} ({obj.open_rate}%) | Clicks: {obj.click_count} ({obj.click_rate}%)"

    @admin.display(description="Preview")
    def preview_link(self, obj):
        if not obj.pk:
            return "Save this campaign to preview it."
        url = reverse("admin:portfolio_app_emailcampaign_preview", args=[obj.pk])
        return format_html('<a class="button" href="{}" target="_blank">Preview email</a>', url)

    @admin.display(description="Test send")
    def send_test_link(self, obj):
        if not obj.pk:
            return "Save this campaign to send a test."
        url = reverse("admin:portfolio_app_emailcampaign_send_test", args=[obj.pk])
        return format_html('<a class="button" href="{}">Send test email</a>', url)

    @admin.display(description="Launch")
    def send_now_link(self, obj):
        if not obj.pk:
            return "Save this campaign to launch it."
        if obj.status == EmailCampaign.CampaignStatus.SENT:
            return "This campaign has already been sent."
        url = reverse("admin:portfolio_app_emailcampaign_send_now", args=[obj.pk])
        return format_html('<a class="button default" href="{}">Send to subscribers now</a>', url)

    @admin.action(description="Send selected campaigns now")
    def send_selected_campaigns(self, request, queryset):
        sent_total = 0
        for campaign in queryset.exclude(status=EmailCampaign.CampaignStatus.SENT):
            sent_total += send_campaign(campaign, request=request)
        self.message_user(request, f"Sent {len(queryset)} campaign(s) to {sent_total} subscribers.", level=messages.SUCCESS)

    @admin.action(description="Duplicate selected campaigns")
    def duplicate_selected_campaigns(self, request, queryset):
        duplicated = 0
        for campaign in queryset:
            featured_projects = list(campaign.featured_projects.all())
            campaign.pk = None
            campaign.status = EmailCampaign.CampaignStatus.DRAFT
            campaign.scheduled_for = None
            campaign.sending_started_at = None
            campaign.sent_at = None
            campaign.recipient_count = 0
            campaign.open_count = 0
            campaign.click_count = 0
            campaign.last_error = ""
            campaign.title = f"{campaign.title} (Copy)"
            campaign.save()
            campaign.featured_projects.set(featured_projects)
            duplicated += 1
        self.message_user(request, f"Duplicated {duplicated} campaign(s).", level=messages.SUCCESS)

    def preview_view(self, request, campaign_id):
        campaign = get_object_or_404(EmailCampaign, pk=campaign_id)
        preview_delivery = EmailDelivery(campaign=campaign, email=request.user.email or "preview@example.com")
        text_body, html_body = build_campaign_email(campaign, request=request, delivery=preview_delivery)
        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "original": campaign,
            "title": f"Preview {campaign.title}",
            "campaign": campaign,
            "html_body": html_body,
            "text_body": text_body,
        }
        return TemplateResponse(request, "admin/portfolio_app/emailcampaign/preview.html", context)

    def send_test_view(self, request, campaign_id):
        campaign = get_object_or_404(EmailCampaign, pk=campaign_id)
        recipients = [email.strip() for email in campaign.test_recipients.split(",") if email.strip()]
        if not recipients and request.user.email:
            recipients = [request.user.email]
        if not recipients:
            self.message_user(request, "Add test recipients or set an email on your admin user account first.", level=messages.WARNING)
            return redirect(reverse("admin:portfolio_app_emailcampaign_change", args=[campaign.pk]))

        sent_count = send_test_campaign(campaign, recipients, request=request)
        self.message_user(request, f"Test email sent to {sent_count} recipient(s).", level=messages.SUCCESS)
        return redirect(reverse("admin:portfolio_app_emailcampaign_change", args=[campaign.pk]))

    def send_now_view(self, request, campaign_id):
        campaign = get_object_or_404(EmailCampaign, pk=campaign_id)
        if campaign.status == EmailCampaign.CampaignStatus.SENT:
            self.message_user(request, "This campaign has already been sent.", level=messages.INFO)
            return redirect(reverse("admin:portfolio_app_emailcampaign_change", args=[campaign.pk]))

        sent_count = send_campaign(campaign, request=request)
        self.message_user(request, f"Campaign sent to {sent_count} subscribers.", level=messages.SUCCESS)
        return redirect(reverse("admin:portfolio_app_emailcampaign_change", args=[campaign.pk]))


@admin.register(PageMetaData)
class PageMetaDataAdmin(admin.ModelAdmin):
    list_display = ("page_name", "meta_title")
    search_fields = ("page_name", "meta_title", "meta_description")

# Register your models here.
