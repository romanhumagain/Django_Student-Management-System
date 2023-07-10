# Generated by Django 4.2.1 on 2023-07-09 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Staff', '0014_notice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment', models.TextField(max_length=500)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Staff.course')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Staff.level')),
            ],
        ),
    ]
