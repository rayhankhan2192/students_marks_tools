# Generated by Django 5.1.6 on 2025-03-13 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0007_student_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='quizapp.batch'),
        ),
    ]
