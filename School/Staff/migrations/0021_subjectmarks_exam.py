# Generated by Django 4.2.1 on 2023-07-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0020_subjectmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectmarks',
            name='exam',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
