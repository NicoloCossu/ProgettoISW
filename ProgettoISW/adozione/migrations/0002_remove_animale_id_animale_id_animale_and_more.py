# Generated by Django 4.2.4 on 2023-09-16 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adozione', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animale',
            name='id',
        ),
        migrations.AddField(
            model_name='animale',
            name='ID_animale',
            field=models.CharField(default='Animale', max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='richiestaadozione',
            name='animale',
            field=models.ForeignKey(default='Animale', null=True, on_delete=django.db.models.deletion.PROTECT, to='adozione.animale'),
        ),
    ]
