from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    AboutSection,
    Certification,
    ContactInformation,
    ContactSubmission,
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


@admin.register(PageMetaData)
class PageMetaDataAdmin(admin.ModelAdmin):
    list_display = ("page_name", "meta_title")
    search_fields = ("page_name", "meta_title", "meta_description")

# Register your models here.
