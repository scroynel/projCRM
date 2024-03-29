# Generated by Django 4.0.6 on 2023-11-22 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('lead', '0002_lead_converted_to_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='teams.team'),
            preserve_default=False,
        ),
    ]
