# Generated by Django 3.2 on 2022-01-23 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stage_api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stage",
            name="name",
        ),
    ]