# Generated by Django 5.1.2 on 2024-11-27 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_payment_payment_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
