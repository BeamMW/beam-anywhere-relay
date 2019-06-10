# Generated by Django 2.1.5 on 2019-04-25 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_status', models.CharField(default='initiated', max_length=192)),
                ('send_to', models.IntegerField()),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('fee', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('send_from', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PushStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('status_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('push_token', models.CharField(max_length=192)),
                ('wallet_address', models.CharField(blank=True, max_length=192)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('msgr_type', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='push_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bar.PushStatus'),
        ),
    ]
