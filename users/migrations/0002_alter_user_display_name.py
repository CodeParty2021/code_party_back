# Generated by Django 3.2 on 2021-12-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="display_name",
            field=models.CharField(max_length=64),
        ),
    ]
