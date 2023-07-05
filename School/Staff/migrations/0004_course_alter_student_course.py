# Generated by Django 4.2.1 on 2023-07-03 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0003_remove_profile_student_id_profile_student_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Staff.course'),
        ),
    ]
