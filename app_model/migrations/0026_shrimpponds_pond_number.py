# Generated by Django 4.2.6 on 2024-10-21 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_model', '0025_alter_shrimppondsdetail_shrimp_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='shrimpponds',
            name='pond_number',
            field=models.IntegerField(null=True),
        ),
    ]
