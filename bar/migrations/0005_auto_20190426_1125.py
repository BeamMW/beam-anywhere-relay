# Generated by Django 2.1.5 on 2019-04-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0004_auto_20190425_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='send_to',
            field=models.CharField(max_length=192),
        ),
    ]
