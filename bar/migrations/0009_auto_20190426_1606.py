# Generated by Django 2.1.5 on 2019-04-26 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0008_auto_20190426_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='push_token',
            field=models.CharField(blank=True, max_length=192, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=192, null=True),
        ),
    ]
