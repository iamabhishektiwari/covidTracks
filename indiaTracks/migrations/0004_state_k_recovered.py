# Generated by Django 3.0.4 on 2020-04-11 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indiaTracks', '0003_auto_20200411_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='state_k',
            name='recovered',
            field=models.IntegerField(default=0),
        ),
    ]
