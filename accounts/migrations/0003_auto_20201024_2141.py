# Generated by Django 3.0.7 on 2020-10-24 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customuser_userflag'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='admissionDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='serialno',
            field=models.TextField(null=True),
        ),
    ]