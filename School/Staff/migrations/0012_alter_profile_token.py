# Generated by Django 4.2.1 on 2023-07-06 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0011_remove_profile_student_profile_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='token',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
