# Generated by Django 5.1.4 on 2025-01-21 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='section',
        ),
        migrations.RemoveField(
            model_name='student',
            name='marks',
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=50)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='quizapp.batch')),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_name', models.CharField(max_length=50)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='quizapp.section')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='quizapp.quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_results', to='quizapp.student')),
            ],
            options={
                'verbose_name': 'Quiz Result',
                'verbose_name_plural': 'Quiz Results',
                'unique_together': {('student', 'quiz')},
            },
        ),
    ]
