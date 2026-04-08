from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0010_remove_aboutsection_achievements_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectDetailImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("image", models.ImageField(upload_to="projects/details/")),
                ("alt_text", models.CharField(blank=True, max_length=180)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="additional_images", to="portfolio_app.project")),
            ],
            options={
                "verbose_name": "Project detail image",
                "verbose_name_plural": "Project detail images",
                "ordering": ["order", "id"],
            },
        ),
    ]
