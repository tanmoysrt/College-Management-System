# Generated by Django 3.0.7 on 2020-10-27 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_registrationlinkshare_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationlinkshare',
            name='key',
        ),
    ]
