# Generated by Django 2.1 on 2018-08-29 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0004_auto_20180829_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='nb_of_guests',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]