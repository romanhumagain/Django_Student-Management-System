# Generated by Django 4.2.1 on 2023-07-04 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0009_level_alter_student_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=100)),
                ('sub_code', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Staff.course')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Staff.level')),
            ],
        ),
    ]