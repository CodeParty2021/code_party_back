from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('user', models.IntegerField()),
                ('file_path', models.IntegerField(max_length=128)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_path', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ResultCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('result', models.IntegerField())
            ],
        ),
    ]