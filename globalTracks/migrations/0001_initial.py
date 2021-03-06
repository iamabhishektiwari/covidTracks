# Generated by Django 3.0.4 on 2020-04-10 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('totalconfirmed', models.IntegerField(default=0)),
                ('totaldeaths', models.IntegerField(default=0)),
                ('totalrecovered', models.IntegerField(default=0)),
                ('latitude', models.DecimalField(decimal_places=2, max_digits=5)),
                ('longitude', models.DecimalField(decimal_places=2, max_digits=5)),
                ('lastupdate', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('totalconfirmed', models.IntegerField(default=0)),
                ('totaldeaths', models.IntegerField(default=0)),
                ('totalrecovered', models.IntegerField(default=0)),
                ('latitude', models.DecimalField(decimal_places=2, max_digits=5)),
                ('longitude', models.DecimalField(decimal_places=2, max_digits=5)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalTracks.Country')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('totalconfirmed', models.IntegerField(default=0)),
                ('totaldeaths', models.IntegerField(default=0)),
                ('totalrecovered', models.IntegerField(default=0)),
                ('latitude', models.DecimalField(decimal_places=2, max_digits=5)),
                ('longitude', models.DecimalField(decimal_places=2, max_digits=5)),
                ('keyid', models.CharField(max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalTracks.Country')),
                ('provice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalTracks.Province')),
            ],
        ),
    ]
