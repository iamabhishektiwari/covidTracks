# Generated by Django 3.0.4 on 2020-04-11 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indiaTracks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State_k',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('confirmed', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('active', models.IntegerField(default=0)),
                ('deltaConfirmed', models.IntegerField(default=0)),
                ('deltaDeaths', models.IntegerField(default=0)),
                ('deltaRecovered', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('confirmed', models.IntegerField(default=0)),
                ('deltaConfirmed', models.IntegerField(default=0)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indiaTracks.State_k')),
            ],
        ),
    ]
