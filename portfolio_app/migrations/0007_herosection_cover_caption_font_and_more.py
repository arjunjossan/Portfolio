from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0006_herosection_cover_caption_herosection_cover_heading_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="cover_caption_font",
            field=models.CharField(
                choices=[
                    ("editorial", "Editorial Serif"),
                    ("fashion", "Fashion Serif"),
                    ("modern", "Modern Sans"),
                    ("poster", "Poster Caps"),
                    ("clean", "Clean Body"),
                ],
                default="clean",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cover_heading_font",
            field=models.CharField(
                choices=[
                    ("editorial", "Editorial Serif"),
                    ("fashion", "Fashion Serif"),
                    ("modern", "Modern Sans"),
                    ("poster", "Poster Caps"),
                    ("clean", "Clean Body"),
                ],
                default="editorial",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cover_heading_offset_x",
            field=models.IntegerField(
                default=0,
                help_text="Move the heading horizontally in pixels. Use negative values to pull it left.",
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cover_heading_offset_y",
            field=models.IntegerField(
                default=0,
                help_text="Move the heading vertically in pixels. Use negative values to pull it upward.",
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="cover_label_font",
            field=models.CharField(
                choices=[
                    ("editorial", "Editorial Serif"),
                    ("fashion", "Fashion Serif"),
                    ("modern", "Modern Sans"),
                    ("poster", "Poster Caps"),
                    ("clean", "Clean Body"),
                ],
                default="modern",
                max_length=20,
            ),
        ),
    ]
