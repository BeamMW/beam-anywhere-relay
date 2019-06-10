from django.db import models
import datetime
import pytz


class PushStatus(models.Model):
    title = models.CharField(blank=False, null=False, max_length=64)
    status_id = models.IntegerField(null=False, blank=False)


class User(models.Model):
    username = models.CharField(blank=True, null=True, max_length=192)
    user_id = models.IntegerField(blank=False, null=False)
    push_token = models.CharField(blank=True, null=True, max_length=192)
    wallet_address = models.CharField(blank=True, max_length=192)
    created_at = models.DateTimeField(auto_now_add=True)
    msgr_type = models.CharField(blank=False, max_length=64)

    def from_json(self, _json):
        self.push_token = _json['push_token']
        self.msgr_type = _json['msgr_type']
        if 'wallet_address' in _json:
            self.wallet_address = _json['wallet_address']
        if 'username' in _json:
            self.username = _json['username']
        if 'user_id' in _json:
            self.user_id = _json['user_id']

    def update_address(self, _address):
        self.wallet_address = _address


class Notification(models.Model):
    transaction_status = models.CharField(blank=False, default='initiated', null=False, max_length=192)
    push_status = models.IntegerField(blank=False, default=1)
    send_from = models.CharField(blank=False, max_length=192)
    amount = models.IntegerField(null=True, blank=True)
    fee = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    push_type = models.IntegerField(blank=False)

    def from_json(self, _json):
        self.push_type = _json['push_type']
        self.amount = _json['amount']
        self.fee = _json['fee']
        if 'send_from' in _json:
            self.send_from = _json['send_from']

    def add_receiver(self, send_from):
        self.send_from = send_from

    def update_transaction_status(self, _status):
        self.transaction_status = _status

    def update_push_status(self, _status):
        self.push_status = _status

    def get_id(self):
        return self.id
