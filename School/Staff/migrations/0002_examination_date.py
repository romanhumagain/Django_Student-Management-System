# Generated by Django 4.2.1 on 2023-07-22 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='date',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]