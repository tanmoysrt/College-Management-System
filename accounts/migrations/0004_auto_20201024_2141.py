# Generated by Django 3.0.7 on 2020-10-24 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201024_2141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofile',
            old_name='admissionDate',
            new_name='admissiondate',
        ),
    ]
