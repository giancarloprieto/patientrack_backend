# Generated by Django 4.2.6 on 2024-01-04 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_alter_staff_date_of_birth_alter_staff_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='last_updated_by',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='last updated by'),
        ),
    ]
