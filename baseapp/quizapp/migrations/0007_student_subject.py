# Generated by Django 5.1.6 on 2025-03-13 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0006_remove_student_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='subject',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='quizapp.subject'),
            preserve_default=False,
        ),
    ]
