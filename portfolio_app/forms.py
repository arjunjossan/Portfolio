from django import forms

from .models import ContactSubmission, Subscriber


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
        fields = ["email"]

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def validate_unique(self):
        pass
