# Generated by Django 3.2 on 2022-03-02 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_is_stuff"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="is_stuff",
            new_name="is_staff",
        ),
    ]
