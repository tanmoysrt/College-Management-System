# Generated by Django 3.0.7 on 2020-10-25 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_delete_teacherprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('cse', 'CSE'), ('it', 'IT')], max_length=50, null=True)),
                ('title', models.TextField(null=True)),
                ('link', models.TextField(default='')),
                ('teachername', models.CharField(max_length=100, null=True)),
                ('teacherid', models.UUIDField(null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]