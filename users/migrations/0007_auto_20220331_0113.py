# Generated by Django 3.2 on 2022-03-30 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_is_stuff_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
