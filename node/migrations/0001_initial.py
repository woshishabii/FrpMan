# Generated by Django 4.0.4 on 2022-05-04 09:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('identifier', models.UUIDField(default=uuid.uuid5, editable=False, primary_key=True, serialize=False)),
                ('pre_name', models.CharField(max_length=10)),
                ('display_name', models.CharField(max_length=10)),
                ('domain_name', models.CharField(max_length=100)),
                ('default_port_start', models.IntegerField()),
                ('default_port_end', models.IntegerField()),
                ('manage_password', models.CharField(max_length=16)),
                ('status', models.CharField(default='Offline', max_length=50)),
                ('announcement', models.TextField(blank=True)),
                ('max_bandwidth', models.IntegerField()),
                ('price', models.IntegerField()),
                ('location', models.CharField(max_length=50)),
            ],
        ),
    ]
