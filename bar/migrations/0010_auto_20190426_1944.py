# Generated by Django 2.1.5 on 2019-04-26 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0009_auto_20190426_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='send_to',
            new_name='send_from',
        ),
    ]