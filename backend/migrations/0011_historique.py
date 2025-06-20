# Generated by Django 5.1.4 on 2025-06-16 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_remove_client_password_client_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Achat', 'Achat'), ('Vente', 'Vente')], max_length=10)),
                ('quantite', models.FloatField()),
                ('montant', models.FloatField()),
                ('statut', models.CharField(choices=[('En attente', 'En attente'), ('Approuvé', 'Approuvé'), ('Rejeté', 'Rejeté')], default='En attente', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.client')),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.crypto')),
            ],
        ),
    ]
