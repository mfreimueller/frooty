# Generated by Django 5.1.7 on 2025-03-24 09:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('family_name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Families',
                'ordering': ['name'],
            },
            bases=('auth.group',),
        ),
    ]
