# Generated by Django 4.2.1 on 2023-07-01 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('profile_pic', models.ImageField(null=True, upload_to='profile')),
                ('student_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Staff.studentid')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200)),
                ('is_verified', models.BooleanField(default=False)),
                ('student_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Staff.studentid')),
            ],
        ),
    ]