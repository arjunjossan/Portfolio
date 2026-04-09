import subprocess
import tempfile
import uuid
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class ActiveOrderedModel(models.Model):
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=120)
    logo_text = models.CharField(max_length=60, blank=True)
    seo_title = models.CharField(max_length=160)
    seo_description = models.TextField()
    seo_keywords = models.CharField(max_length=255, blank=True)
    accent_text = models.CharField(max_length=60, blank=True)
    availability_status = models.CharField(max_length=120, blank=True)
    footer_note = models.CharField(max_length=160, blank=True)
    resume_label = models.CharField(max_length=40, default="Download CV")
    show_theme_toggle = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site configuration"
        verbose_name_plural = "Site configuration"

    def __str__(self):
        return self.site_name


class HeroSection(models.Model):
    class CoverStyle(models.TextChoices):
        CLASSIC = "classic", "Classic"
        BOLD = "bold", "Bold"
        MINIMAL = "minimal", "Minimal"

    class CoverFont(models.TextChoices):
        EDITORIAL = "editorial", "Editorial Serif"
        FASHION = "fashion", "Fashion Serif"
        MODERN = "modern", "Modern Sans"
        POSTER = "poster", "Poster Caps"
        CLEAN = "clean", "Clean Body"

    title = models.CharField(max_length=180)
    subtitle = models.TextField()
    headline_image = models.FileField(upload_to="profile/hero/", blank=True, null=True)
    cover_label = models.CharField(max_length=80, blank=True, help_text="Small top label shown on the hero image.")
    cover_heading = models.CharField(max_length=120, blank=True, help_text="Large editorial title placed on the hero image.")
    cover_caption = models.CharField(max_length=220, blank=True, help_text="Short line shown near the bottom of the hero image.")
    cover_style = models.CharField(max_length=20, choices=CoverStyle.choices, default=CoverStyle.CLASSIC)
    cover_label_font = models.CharField(max_length=20, choices=CoverFont.choices, default=CoverFont.MODERN)
    cover_heading_font = models.CharField(max_length=20, choices=CoverFont.choices, default=CoverFont.EDITORIAL)
    cover_caption_font = models.CharField(max_length=20, choices=CoverFont.choices, default=CoverFont.CLEAN)
    cover_text_opacity = models.PositiveSmallIntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Overall opacity for the image cover text from 0 to 100.",
    )
    cover_heading_offset_x = models.IntegerField(default=0, help_text="Move the heading horizontally in pixels. Use negative values to pull it left.")
    cover_heading_offset_y = models.IntegerField(default=0, help_text="Move the heading vertically in pixels. Use negative values to pull it upward.")
    cta_button_text = models.CharField(max_length=50)
    cta_button_url = models.CharField(max_length=255)
    secondary_button_text = models.CharField(max_length=50, blank=True)
    secondary_button_url = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Hero section"
        verbose_name_plural = "Hero section"

    def __str__(self):
        return self.title

    def _convert_hero_image_for_web(self):
        if not self.headline_image:
            return

        extension = Path(self.headline_image.name).suffix.lower()
        if extension not in {".heic", ".heif"}:
            return

        self.headline_image.open("rb")
        uploaded_bytes = self.headline_image.read()

        with tempfile.NamedTemporaryFile(suffix=extension) as source_file, tempfile.NamedTemporaryFile(
            suffix=".jpg"
        ) as converted_file:
            source_file.write(uploaded_bytes)
            source_file.flush()

            subprocess.run(
                [
                    "sips",
                    "-s",
                    "format",
                    "jpeg",
                    source_file.name,
                    "--out",
                    converted_file.name,
                ],
                check=True,
                capture_output=True,
            )

            converted_file.seek(0)
            self.headline_image.save(
                f"{Path(self.headline_image.name).stem}.jpg",
                ContentFile(converted_file.read()),
                save=False,
            )

    def save(self, *args, **kwargs):
        self._convert_hero_image_for_web()
        super().save(*args, **kwargs)


class AboutSection(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField()
    profile_image = models.ImageField(upload_to="profile/about/", blank=True, null=True)
    background_summary = models.TextField()
    quick_facts = models.JSONField(default=dict, blank=True)
    masters_goals = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About section"
        verbose_name_plural = "About section"

    def __str__(self):
        return self.title


class TechnicalSkill(ActiveOrderedModel):
    class SkillCategory(models.TextChoices):
        BACKEND = "Backend", "Backend"
        FRONTEND = "Frontend", "Frontend"
        TOOLS = "Tools", "Tools"
        DATA = "Data Analysis", "Data Analysis"
        CLOUD = "Cloud", "Cloud"

    category = models.CharField(max_length=30, choices=SkillCategory.choices)
    skill_name = models.CharField(max_length=120)
    proficiency_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    icon = models.CharField(
        max_length=80,
        blank=True,
        help_text="Font Awesome class name such as fa-brands fa-python",
    )
    description = models.TextField(blank=True)
    years_of_experience = models.PositiveSmallIntegerField(default=1)

    class Meta(ActiveOrderedModel.Meta):
        unique_together = ("category", "skill_name")

    def __str__(self):
        return f"{self.skill_name} ({self.category})"


class Project(ActiveOrderedModel):
    class ProjectCategory(models.TextChoices):
        FULL_STACK = "Full-Stack", "Full-Stack"
        BACKEND = "Backend", "Backend"
        FRONTEND = "Frontend", "Frontend"
        DATA = "Data", "Data"

    class ProjectStatus(models.TextChoices):
        COMPLETED = "Completed", "Completed"
        IN_PROGRESS = "In Progress", "In Progress"
        ARCHIVED = "Archived", "Archived"

    title = models.CharField(max_length=180)
    description = models.TextField()
    project_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    technologies_used = models.JSONField(default=list, blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.COMPLETED)
    category = models.CharField(max_length=20, choices=ProjectCategory.choices, default=ProjectCategory.FULL_STACK)
    detailed_description = models.TextField()
    key_features = models.JSONField(default=list, blank=True)
    lessons_learned = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True)

    class Meta(ActiveOrderedModel.Meta):
        ordering = ["order", "-start_date", "id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 2
            while Project.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio_app:project_detail", kwargs={"slug": self.slug})

    @property
    def gallery_images(self):
        additional_images = list(self.additional_images.filter(is_active=True))
        if self.project_image:
            return [
                {
                    "id": f"project-primary-{self.pk or 'new'}",
                    "image": self.project_image,
                    "alt_text": self.title,
                    "is_primary": True,
                },
                *[
                    {
                        "id": f"project-extra-{image.pk}",
                        "image": image.image,
                        "alt_text": image.alt_text or self.title,
                        "is_primary": False,
                    }
                    for image in additional_images
                ],
            ]
        return [
            {
                "id": f"project-extra-{image.pk}",
                "image": image.image,
                "alt_text": image.alt_text or self.title,
                "is_primary": False,
            }
            for image in additional_images
        ]


class ProjectDetailImage(ActiveOrderedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="additional_images")
    image = models.ImageField(upload_to="projects/details/")
    alt_text = models.CharField(max_length=180, blank=True)

    class Meta(ActiveOrderedModel.Meta):
        verbose_name = "Project detail image"
        verbose_name_plural = "Project detail images"

    def __str__(self):
        return f"{self.project.title} image {self.order or self.pk}"


class Experience(ActiveOrderedModel):
    job_title = models.CharField(max_length=140)
    company_name = models.CharField(max_length=140)
    location = models.CharField(max_length=140)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    key_responsibilities = models.JSONField(default=list, blank=True)
    technologies_used = models.JSONField(default=list, blank=True)
    company_logo = models.ImageField(upload_to="experiences/", blank=True, null=True)

    class Meta(ActiveOrderedModel.Meta):
        ordering = ["order", "-start_date", "id"]

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Education(ActiveOrderedModel):
    degree_name = models.CharField(max_length=160)
    institution_name = models.CharField(max_length=180)
    location = models.CharField(max_length=140)
    field_of_study = models.CharField(max_length=140)
    start_date = models.DateField()
    end_date = models.DateField()
    gpa_cgpa = models.CharField(max_length=40, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    relevant_coursework = models.JSONField(default=list, blank=True)
    institution_logo = models.ImageField(upload_to="education/", blank=True, null=True)

    class Meta(ActiveOrderedModel.Meta):
        ordering = ["order", "-end_date", "id"]

    def __str__(self):
        return f"{self.degree_name} - {self.institution_name}"


class Certification(ActiveOrderedModel):
    title = models.CharField(max_length=180)
    issuer = models.CharField(max_length=160)
    issue_date = models.DateField()
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    badge_image = models.ImageField(upload_to="certifications/", blank=True, null=True)

    def __str__(self):
        return self.title


class ContactInformation(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=140, blank=True)
    resume_pdf = models.FileField(upload_to="documents/", blank=True, null=True)
    cv_download_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Contact information"
        verbose_name_plural = "Contact information"

    def __str__(self):
        return self.email


class SocialMediaLink(ActiveOrderedModel):
    platform = models.CharField(max_length=60)
    profile_url = models.URLField()
    icon_code = models.CharField(
        max_length=80,
        help_text="Font Awesome class name such as fa-brands fa-linkedin-in",
    )

    def __str__(self):
        return self.platform


class ContactSubmission(models.Model):
    class MessageType(models.TextChoices):
        PROJECT = "Project Inquiry", "Project Inquiry"
        COLLABORATION = "Collaboration", "Collaboration"
        GENERAL = "General", "General"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=120, blank=True)
    message_type = models.CharField(
        max_length=30,
        choices=MessageType.choices,
        default=MessageType.GENERAL,
    )
    subject = models.CharField(max_length=160)
    message = models.TextField()
    attachment = models.FileField(upload_to="contact_attachments/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    response_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email

    def unsubscribe_path(self):
        return reverse("portfolio_app:unsubscribe", args=[self.unsubscribe_token])


class EmailCampaign(models.Model):
    class CampaignType(models.TextChoices):
        PORTFOLIO_UPDATE = "portfolio_update", "Portfolio update"
        ANNOUNCEMENT = "announcement", "Announcement"
        MARKETING = "marketing", "Marketing"

    class CampaignAudience(models.TextChoices):
        ALL_ACTIVE = "all_active", "All active subscribers"
        NEWEST_30_DAYS = "newest_30_days", "Subscribers from the last 30 days"
        NEWEST_90_DAYS = "newest_90_days", "Subscribers from the last 90 days"

    class CampaignStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        SCHEDULED = "scheduled", "Scheduled"
        SENDING = "sending", "Sending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    class TemplateStyle(models.TextChoices):
        EDITORIAL = "editorial", "Editorial"
        MINIMAL = "minimal", "Minimal"
        LAUNCH = "launch", "Launch"

    title = models.CharField(max_length=160)
    campaign_type = models.CharField(max_length=30, choices=CampaignType.choices, default=CampaignType.MARKETING)
    audience = models.CharField(max_length=30, choices=CampaignAudience.choices, default=CampaignAudience.ALL_ACTIVE)
    subject = models.CharField(max_length=200)
    preview_text = models.CharField(max_length=220, blank=True)
    internal_notes = models.TextField(blank=True, help_text="Only visible in admin/dashboard. Use it for planning and follow-ups.")
    template_style = models.CharField(max_length=20, choices=TemplateStyle.choices, default=TemplateStyle.EDITORIAL)
    headline = models.CharField(max_length=160, blank=True)
    intro = models.TextField(blank=True, help_text="Short intro shown above the main content.")
    content = models.TextField(
        help_text="Use plain text or simple paragraphs. Line breaks will be preserved in the email."
    )
    cta_label = models.CharField(max_length=60, blank=True)
    cta_url = models.URLField(blank=True)
    featured_projects = models.ManyToManyField(Project, blank=True, related_name="email_campaigns")
    include_latest_projects = models.BooleanField(default=True)
    latest_projects_count = models.PositiveSmallIntegerField(default=3)
    test_recipients = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated email addresses for preview sends before a full launch.",
    )
    track_opens = models.BooleanField(default=True)
    track_clicks = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=CampaignStatus.choices, default=CampaignStatus.DRAFT)
    scheduled_for = models.DateTimeField(blank=True, null=True)
    sending_started_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    recipient_count = models.PositiveIntegerField(default=0)
    open_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_email_campaigns",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.scheduled_for and self.status == self.CampaignStatus.DRAFT:
            self.status = self.CampaignStatus.SCHEDULED
        if not self.scheduled_for and self.status == self.CampaignStatus.SCHEDULED and not self.sent_at:
            self.status = self.CampaignStatus.DRAFT
        if self.status == self.CampaignStatus.SENT and not self.sent_at:
            self.sent_at = timezone.now()
        super().save(*args, **kwargs)

    def get_featured_projects(self):
        selected_projects = list(self.featured_projects.filter(is_active=True).order_by("order", "-start_date", "id"))
        selected_ids = {project.id for project in selected_projects}
        if self.include_latest_projects and self.latest_projects_count:
            latest_projects = list(
                Project.objects.filter(is_active=True)
                .exclude(id__in=selected_ids)
                .order_by("-start_date", "order", "id")[: self.latest_projects_count]
            )
            selected_projects.extend(latest_projects)
        return selected_projects

    def get_target_subscribers(self):
        subscribers = Subscriber.objects.filter(is_active=True)
        if self.audience == self.CampaignAudience.NEWEST_30_DAYS:
            subscribers = subscribers.filter(subscribed_at__gte=timezone.now() - timezone.timedelta(days=30))
        elif self.audience == self.CampaignAudience.NEWEST_90_DAYS:
            subscribers = subscribers.filter(subscribed_at__gte=timezone.now() - timezone.timedelta(days=90))
        return subscribers.order_by("email")

    @property
    def total_deliveries(self):
        return self.deliveries.count()

    @property
    def open_rate(self):
        if not self.recipient_count:
            return 0
        return round((self.open_count / self.recipient_count) * 100, 1)

    @property
    def click_rate(self):
        if not self.recipient_count:
            return 0
        return round((self.click_count / self.recipient_count) * 100, 1)

    def status_badge(self):
        return self.get_status_display()


class EmailDelivery(models.Model):
    class DeliveryStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"
        TEST = "test", "Test"

    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, related_name="deliveries")
    subscriber = models.ForeignKey(
        Subscriber,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="email_deliveries",
    )
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING)
    subject_snapshot = models.CharField(max_length=200, blank=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    opened_at = models.DateTimeField(blank=True, null=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    open_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["campaign", "email"], name="unique_campaign_email_delivery"),
        ]

    def __str__(self):
        return f"{self.campaign.title} -> {self.email}"


class PageMetaData(models.Model):
    page_name = models.CharField(max_length=60, unique=True)
    meta_title = models.CharField(max_length=160)
    meta_description = models.TextField()
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)
    og_description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Page metadata"
        verbose_name_plural = "Page metadata"

    def __str__(self):
        return self.page_name

# Create your models here.
