from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0008_herosection_cover_text_opacity"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Testimonial",
        ),
    ]
