# Generated by Django 4.2.4 on 2023-09-17 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adozione', '0008_alter_richiestaadozione_utente'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Utente',
        ),
    ]
