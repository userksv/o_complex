# Generated by Django 5.0.7 on 2024-07-19 02:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_visit', models.DateTimeField(auto_now=True)),
                ('last_city', models.CharField(max_length=100)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
            ],
        ),
    ]
