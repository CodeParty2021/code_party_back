# Generated by Django 3.2 on 2022-03-07 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_rename_is_staff_user_is_stuff"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="is_stuff",
            new_name="is_staff",
        ),
    ]
