# Generated by Django 2.1 on 2018-08-31 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0011_auto_20180830_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.DecimalField(decimal_places=1, max_digits=5, verbose_name='quantité par personne en grammes (ou en nb pour les oeufs)'),
        ),
    ]
