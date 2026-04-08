from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_app", "0011_projectdetailimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="show_theme_toggle",
            field=models.BooleanField(default=True),
        ),
    ]
