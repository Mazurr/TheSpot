# Generated by Django 3.1.1 on 2020-09-13 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200913_1431'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-create_date']},
        ),
    ]
