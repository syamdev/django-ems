# Generated by Django 3.1.4 on 2021-01-02 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_ems', '0003_employee_departments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Salaries',
            new_name='Salary',
        ),
        migrations.RenameField(
            model_name='salary',
            old_name='salary',
            new_name='salary_amount',
        ),
    ]