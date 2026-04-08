from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0005_alter_herosection_headline_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="cover_caption",
            field=models.CharField(blank=True, help_text="Short line shown near the bottom of the hero image.", max_length=220),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cover_heading",
            field=models.CharField(blank=True, help_text="Large editorial title placed on the hero image.", max_length=120),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cover_label",
            field=models.CharField(blank=True, help_text="Small top label shown on the hero image.", max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cover_style",
            field=models.CharField(choices=[("classic", "Classic"), ("bold", "Bold"), ("minimal", "Minimal")], default="classic", max_length=20),
        ),
    ]
