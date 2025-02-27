# Generated by Django 5.1.4 on 2025-02-03 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountsapp', '0002_otp'),
        ('quizapp', '0002_batch_auth_users_quiz_auth_users_student_auth_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='auth_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='accountsapp.account'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='auth_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizs', to='accountsapp.account'),
        ),
        migrations.AlterField(
            model_name='student',
            name='auth_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='accountsapp.account'),
        ),
    ]
