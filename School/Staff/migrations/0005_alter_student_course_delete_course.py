# Generated by Django 4.2.1 on 2023-07-03 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0004_course_alter_student_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]