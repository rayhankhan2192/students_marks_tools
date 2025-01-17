# Generated by Django 5.1.4 on 2025-01-17 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=100)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='quizapp.batch')),
            ],
        ),
        migrations.CreateModel(
            name='Quizs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='quizapp.section')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('student_id', models.CharField(max_length=20, unique=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='quizapp.section')),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.DecimalField(decimal_places=2, max_digits=5)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='quizapp.quizs')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='quizapp.student')),
            ],
            options={
                'unique_together': {('student', 'quiz')},
            },
        ),
    ]
