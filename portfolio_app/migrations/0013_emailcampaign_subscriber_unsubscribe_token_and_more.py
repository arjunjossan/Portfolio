import uuid

from django.db import migrations, models


def populate_subscriber_unsubscribe_tokens(apps, schema_editor):
    Subscriber = apps.get_model("portfolio_app", "Subscriber")
    for subscriber in Subscriber.objects.filter(unsubscribe_token__isnull=True):
        subscriber.unsubscribe_token = uuid.uuid4()
        subscriber.save(update_fields=["unsubscribe_token"])


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0012_siteconfiguration_show_theme_toggle"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailCampaign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("subject", models.CharField(max_length=200)),
                ("preview_text", models.CharField(blank=True, max_length=220)),
                (
                    "content",
                    models.TextField(
                        help_text="Use plain text or simple paragraphs. Line breaks will be preserved in the email."
                    ),
                ),
                ("cta_label", models.CharField(blank=True, max_length=60)),
                ("cta_url", models.URLField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("sent", "Sent")],
                        default="draft",
                        max_length=20,
                    ),
                ),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("recipient_count", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="subscriber",
            name="unsubscribed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="subscriber",
            name="unsubscribe_token",
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.RunPython(
            populate_subscriber_unsubscribe_tokens,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="subscriber",
            name="unsubscribe_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
