from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0007_herosection_cover_caption_font_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="cover_text_opacity",
            field=models.PositiveSmallIntegerField(
                default=100,
                help_text="Overall opacity for the image cover text from 0 to 100.",
                validators=[MinValueValidator(0), MaxValueValidator(100)],
            ),
        ),
    ]
