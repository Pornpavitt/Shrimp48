# Generated by Django 4.2.6 on 2025-01-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_model', '0028_alter_shrimppondsdetail_growth_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='shrimppondsdetail',
            name='predicted_growth_rate_date_base',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='shrimppondsdetail',
            name='predicted_growth_rate_weight_base',
            field=models.FloatField(null=True),
        ),
    ]
