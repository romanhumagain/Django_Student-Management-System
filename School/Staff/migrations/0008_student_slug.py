# Generated by Django 4.2.1 on 2023-08-02 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0007_alter_submittedassignment_assignment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='slug',
            field=models.SlugField(default=None, null=True, unique=True),
        ),
    ]
