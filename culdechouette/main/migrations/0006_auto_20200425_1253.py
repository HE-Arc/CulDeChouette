# Generated by Django 3.0.5 on 2020-04-25 12:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200425_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.UUIDField(default=uuid.UUID('568d5a29-d9f4-4811-9580-670c931ae361'), editable=False, primary_key=True, serialize=False),
        ),
    ]