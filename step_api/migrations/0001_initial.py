# Generated by Django 3.2 on 2022-02-12 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("stage_api", "0004_stage_movie_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="Step",
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
                ("objective", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=300)),
                ("index", models.IntegerField()),
                (
                    "stage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stage_api.stage",
                    ),
                ),
            ],
        ),
    ]
