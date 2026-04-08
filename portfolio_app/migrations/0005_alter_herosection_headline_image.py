from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0004_subscriber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="herosection",
            name="headline_image",
            field=models.FileField(blank=True, null=True, upload_to="profile/hero/"),
        ),
    ]
