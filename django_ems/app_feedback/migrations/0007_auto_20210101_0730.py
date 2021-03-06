# Generated by Django 3.1.4 on 2021-01-01 07:30

import app_feedback.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_feedback', '0006_auto_20210101_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='email',
            field=models.CharField(max_length=150, validators=[django.core.validators.EmailValidator(whitelist=['sy4m', 'webitu']), django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(100), app_feedback.models.validate_allowed_domains]),
        ),
    ]
