import json

from django import forms
from django.core.exceptions import ValidationError
from django.db import models

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
    WhatsAppWidget,
)


class PrettyJSONField(forms.CharField):
    def __init__(self, *args, initial_type="list", **kwargs):
        self.initial_type = initial_type
        kwargs.setdefault("required", False)
        kwargs.setdefault("widget", forms.Textarea(attrs={"rows": 6}))
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if value in (None, ""):
            value = {} if self.initial_type == "dict" else []
        if isinstance(value, str):
            return value
        return json.dumps(value, indent=2, ensure_ascii=True)

    def to_python(self, value):
        value = (value or "").strip()
        if not value:
            return {} if self.initial_type == "dict" else []
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValidationError(f"Enter valid JSON. {error.msg}.") from error

        expected_type = dict if self.initial_type == "dict" else list
        if not isinstance(parsed, expected_type):
            label = "object" if self.initial_type == "dict" else "array"
            raise ValidationError(f"Enter a JSON {label}.")
        return parsed


class DashboardModelForm(forms.ModelForm):
    text_input_classes = (
        "block w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 "
        "text-slate-900 placeholder:text-slate-400 focus:border-teal focus:ring-teal"
    )
    textarea_classes = (
        "block w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 "
        "text-slate-900 placeholder:text-slate-400 focus:border-teal focus:ring-teal"
    )
    checkbox_classes = "h-4 w-4 rounded border-slate-300 text-teal focus:ring-teal"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = self.checkbox_classes
                continue

            if isinstance(widget, (forms.Textarea,)):
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = f"{existing} {self.textarea_classes}".strip()
            else:
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = f"{existing} {self.text_input_classes}".strip()

            if isinstance(widget, forms.ClearableFileInput):
                widget.attrs["class"] = self.text_input_classes
class ContactSubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shared_classes = (
            "block w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 "
            "text-white placeholder:text-slate-500 focus:border-teal focus:ring-teal"
        )
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {shared_classes}".strip()

    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "phone", "company", "message_type", "subject", "message", "attachment"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+91 98765 43210"}),
            "company": forms.TextInput(attrs={"placeholder": "University, company, or organization"}),
            "message_type": forms.Select(),
            "subject": forms.TextInput(attrs={"placeholder": "How can I help?"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Tell me about your opportunity or question."}),
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 20:
            raise forms.ValidationError("Please share a bit more detail so I can respond thoughtfully.")
        return message


class SubscriberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["name"].widget.attrs.update(
            {
                "class": (
                    "block w-full rounded-full border border-white/10 bg-slate-900/80 px-5 py-4 "
                    "text-white placeholder:text-slate-500 focus:border-teal focus:ring-teal"
                ),
                "placeholder": "Enter your full name",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": (
                    "block w-full rounded-full border border-white/10 bg-slate-900/80 px-5 py-4 "
                    "text-white placeholder:text-slate-500 focus:border-teal focus:ring-teal"
                ),
                "placeholder": "Enter your email for project updates",
            }
        )

    class Meta:
        model = Subscriber
        fields = ["name", "email"]

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def validate_unique(self):
        pass


class SiteConfigurationDashboardForm(DashboardModelForm):
    class Meta:
        model = SiteConfiguration
        fields = "__all__"


class WhatsAppWidgetDashboardForm(DashboardModelForm):
    class Meta:
        model = WhatsAppWidget
        fields = "__all__"


class HeroSectionDashboardForm(DashboardModelForm):
    class Meta:
        model = HeroSection
        fields = "__all__"


class AboutSectionDashboardForm(DashboardModelForm):
    quick_facts = PrettyJSONField(initial_type="dict", help_text="JSON object like {\"Projects\": \"12+\"}")

    class Meta:
        model = AboutSection
        fields = "__all__"


class TechnicalSkillDashboardForm(DashboardModelForm):
    class Meta:
        model = TechnicalSkill
        fields = "__all__"


class ProjectDashboardForm(DashboardModelForm):
    technologies_used = PrettyJSONField(initial_type="list", help_text="JSON array like [\"Django\", \"PostgreSQL\"]")
    key_features = PrettyJSONField(initial_type="list", help_text="JSON array of short feature lines.")

    class Meta:
        model = Project
        fields = "__all__"


class ProjectDetailImageDashboardForm(DashboardModelForm):
    class Meta:
        model = ProjectDetailImage
        fields = "__all__"


class ExperienceDashboardForm(DashboardModelForm):
    key_responsibilities = PrettyJSONField(initial_type="list", help_text="JSON array of responsibilities.")
    technologies_used = PrettyJSONField(initial_type="list", help_text="JSON array like [\"Python\", \"Docker\"]")

    class Meta:
        model = Experience
        fields = "__all__"


class EducationDashboardForm(DashboardModelForm):
    highlights = PrettyJSONField(initial_type="list", help_text="JSON array of academic highlights.")
    relevant_coursework = PrettyJSONField(initial_type="list", help_text="JSON array of coursework items.")

    class Meta:
        model = Education
        fields = "__all__"


class CertificationDashboardForm(DashboardModelForm):
    class Meta:
        model = Certification
        fields = "__all__"


class ContactInformationDashboardForm(DashboardModelForm):
    class Meta:
        model = ContactInformation
        fields = "__all__"


class SocialMediaLinkDashboardForm(DashboardModelForm):
    class Meta:
        model = SocialMediaLink
        fields = "__all__"


class ContactSubmissionDashboardForm(DashboardModelForm):
    class Meta:
        model = ContactSubmission
        fields = "__all__"


class SubscriberDashboardForm(DashboardModelForm):
    class Meta:
        model = Subscriber
        fields = "__all__"


class PageMetaDataDashboardForm(DashboardModelForm):
    class Meta:
        model = PageMetaData
        fields = "__all__"
