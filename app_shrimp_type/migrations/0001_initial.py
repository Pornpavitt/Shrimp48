# Generated by Django 4.2.6 on 2024-01-05 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShrimpSpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('food', models.TextField(max_length=255)),
                ('description', models.TextField(max_length=255)),
            ],
        ),
    ]