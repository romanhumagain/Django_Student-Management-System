# Generated by Django 4.2.1 on 2023-08-02 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0010_totalmark_course_totalmark_level'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='totalmark',
            unique_together={('course', 'level', 'student', 'exam')},
        ),
    ]
