# Generated by Django 4.2.4 on 2023-09-19 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adozione', '0012_alter_richiestaadozione_animale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animale',
            name='ID_animale',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
