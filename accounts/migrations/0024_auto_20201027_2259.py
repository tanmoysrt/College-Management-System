# Generated by Django 3.0.7 on 2020-10-27 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_remove_registrationlinkshare_key'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='registrationLinkShare',
            new_name='registrationLinkStudent',
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='serialno',
            field=models.TextField(null=True, unique=True),
        ),
    ]
