# Generated by Django 5.1 on 2024-08-29 11:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_transaction_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
