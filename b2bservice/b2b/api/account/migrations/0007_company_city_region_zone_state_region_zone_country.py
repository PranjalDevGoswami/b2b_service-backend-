# Generated by Django 5.0.6 on 2024-05-22 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_country_created_at_country_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_city', to='account.city'),
        ),
        migrations.AddField(
            model_name='region',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='account.zone'),
        ),
        migrations.AddField(
            model_name='state',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='states', to='account.region'),
        ),
        migrations.AddField(
            model_name='zone',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='account.country'),
        ),
    ]
