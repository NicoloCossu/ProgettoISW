# Generated by Django 4.2.4 on 2023-09-19 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adozione', '0014_alter_richiestaadozione_animale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richiestaadozione',
            name='animale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adozione.animale'),
        ),
    ]
