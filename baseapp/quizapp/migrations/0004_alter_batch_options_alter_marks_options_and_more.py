# Generated by Django 5.1.4 on 2025-01-17 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_alter_batch_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'verbose_name': 'Batch', 'verbose_name_plural': 'Batches'},
        ),
        migrations.AlterModelOptions(
            name='marks',
            options={'verbose_name': 'Marks', 'verbose_name_plural': 'Markss'},
        ),
        migrations.AlterModelOptions(
            name='quizs',
            options={'verbose_name': 'Quizs', 'verbose_name_plural': 'Quizss'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name': 'Section', 'verbose_name_plural': 'Sections'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
    ]
