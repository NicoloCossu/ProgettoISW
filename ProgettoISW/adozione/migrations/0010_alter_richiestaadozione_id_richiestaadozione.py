# Generated by Django 4.2.4 on 2023-09-17 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adozione', '0009_delete_utente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richiestaadozione',
            name='ID_richiestaAdozione',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
