# Generated by Django 4.2.1 on 2023-07-29 08:18

import Staff.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0004_assignment_posted_date_alter_assignment_due_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmittedAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_date', models.DateField(default=None)),
                ('submitted_assignment', models.FileField(upload_to=Staff.models.Assignment)),
                ('assignment_description', models.TextField(max_length=500)),
                ('submission_status', models.CharField(default='pending', max_length=100)),
                ('assignment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Staff.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Staff.student')),
            ],
        ),
    ]