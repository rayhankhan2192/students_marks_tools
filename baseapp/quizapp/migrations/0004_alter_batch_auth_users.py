# Generated by Django 5.1.4 on 2025-02-03 16:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_alter_batch_auth_users_alter_quiz_auth_users_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='auth_users',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='batches', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
