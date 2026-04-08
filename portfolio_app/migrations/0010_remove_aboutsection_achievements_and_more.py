from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0009_delete_testimonial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aboutsection",
            name="achievements",
        ),
        migrations.RemoveField(
            model_name="aboutsection",
            name="focus_areas",
        ),
    ]
