# Generated by Django 5.1.4 on 2025-03-11 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_tutoriel_remove_validateur_autorisation_validation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='prix_achat_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crypto',
            name='prix_vente_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crypto',
            name='quantite',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
