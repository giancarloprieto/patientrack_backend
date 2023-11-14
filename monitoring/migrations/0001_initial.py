# Generated by Django 4.2.6 on 2023-11-14 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('created_by', models.EmailField(blank=True, max_length=254, null=True, verbose_name='created by')),
                ('last_updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('last_updated_by', models.EmailField(blank=True, max_length=254, null=True, verbose_name='created by')),
                ('reference_value', models.FloatField(verbose_name='reference value')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('operator', models.CharField(choices=[('E', 'E'), ('GT', 'GT'), ('GTE', 'GTE'), ('LT', 'LT'), ('LTE', 'LTE')], verbose_name='gender')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('created_by', models.EmailField(blank=True, max_length=254, null=True, verbose_name='created by')),
                ('last_updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('last_updated_by', models.EmailField(blank=True, max_length=254, null=True, verbose_name='created by')),
                ('datetime_server', models.DateTimeField(verbose_name='date and time of server')),
                ('datetime_device', models.DateTimeField(verbose_name='date and time of device')),
                ('patient_identification', models.CharField(max_length=100, verbose_name="patient's identification")),
                ('device_identifier', models.CharField(max_length=100, verbose_name="device's identifier")),
                ('variable_name', models.CharField(max_length=100, verbose_name="variable's name")),
                ('value', models.FloatField(verbose_name='value')),
                ('payload', models.TextField(verbose_name='payload')),
                ('alarm_name', models.CharField(default='', verbose_name="alarm's name")),
                ('alarm_operator', models.CharField(choices=[('E', 'E'), ('GT', 'GT'), ('GTE', 'GTE'), ('LT', 'LT'), ('LTE', 'LTE')], default='', verbose_name="alarm's operator")),
                ('alarm_ref_value', models.FloatField(null=True, verbose_name='reference value')),
                ('alarm_settings_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alarm_settings_record_set', to='monitoring.alarmsettings', verbose_name='alarm settings')),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='device_record_set', to='device.device', verbose_name='device')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]