# Generated by Django 5.1.4 on 2025-06-04 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_kyc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=200)),
                ('nom', models.CharField(help_text='Nom pour identifier cette adresse', max_length=100)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adresses', to='backend.client')),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adresses_crypto', to='backend.crypto')),
            ],
            options={
                'ordering': ['-date_creation'],
                'unique_together': {('client', 'nom')},
            },
        ),
    ]
