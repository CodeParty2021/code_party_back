# Generated by Django 3.2 on 2022-03-03 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_rename_is_stuff_user_is_staff"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="is_staff",
            new_name="is_stuff",
        ),
    ]
