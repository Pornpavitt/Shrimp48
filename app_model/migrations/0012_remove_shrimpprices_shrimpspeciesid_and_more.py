# Generated by Django 4.2.6 on 2024-03-14 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_model', '0011_remove_shrimpponds_pond_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shrimpprices',
            name='ShrimpSpeciesId',
        ),
        migrations.AddField(
            model_name='shrimpprices',
            name='price_specie',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
