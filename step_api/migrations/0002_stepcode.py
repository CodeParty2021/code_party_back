# Generated by Django 3.2 on 2022-05-04 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("code_api", "0001_initial"),
        ("step_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StepCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="code_api.code",
                    ),
                ),
                (
                    "step",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="step_api.step",
                    ),
                ),
            ],
        ),
    ]
