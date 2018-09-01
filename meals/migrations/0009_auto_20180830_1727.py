# Generated by Django 2.1 on 2018-08-30 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0008_auto_20180830_1404'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listelement',
            options={'verbose_name_plural': 'liste de courses'},
        ),
        migrations.RemoveField(
            model_name='food',
            name='fresh',
        ),
        migrations.AddField(
            model_name='food',
            name='category',
            field=models.IntegerField(choices=[(0, 'fruits et légumes'), (1, 'crèmerie'), (2, 'boucherie / charcuterie / poissons'), (3, 'pates / riz / céréales'), (4, 'épicerie'), (5, 'autre')], default=1),
            preserve_default=False,
        ),
    ]