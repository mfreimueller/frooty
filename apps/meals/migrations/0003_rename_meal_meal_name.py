# Generated by Django 5.1.7 on 2025-03-19 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_alter_meal_apples_alter_meal_beans_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meal',
            old_name='meal',
            new_name='name',
        ),
    ]
