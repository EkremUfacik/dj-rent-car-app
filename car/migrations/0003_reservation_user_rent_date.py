# Generated by Django 4.1.5 on 2023-01-30 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0002_reservation'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='reservation',
            constraint=models.UniqueConstraint(fields=('customer', 'start_date', 'end_date'), name='user_rent_date'),
        ),
    ]
