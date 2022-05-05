# Generated by Django 4.0.4 on 2022-05-05 09:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='pre_name',
            new_name='prefix',
        ),
        migrations.AlterField(
            model_name='node',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]