# Generated by Django 4.2.6 on 2024-02-17 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0007_variable_css_class_suffix_variable_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='color',
            field=models.CharField(default='blue', max_length=100, verbose_name='color'),
            preserve_default=False,
        ),
    ]
