# Generated by Django 4.2.6 on 2024-03-12 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_model', '0006_alter_shrimpspecies_specie_food'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shrimppondsdetail',
            old_name='pondId',
            new_name='pond',
        ),
    ]