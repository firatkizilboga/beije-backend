# Generated by Django 4.1.7 on 2023-03-12 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='next_fulfillment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
