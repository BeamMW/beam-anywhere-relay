# Create your views here.
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

import requests
import json
import os

from .models import *
from .serializers import *

SHOUT_PUSH_ID = 1
SILENT_PUSH_ID = 0

settings_dir = os.path.dirname(__file__)
proj_root = os.path.abspath(os.path.dirname(settings_dir))
with open(os.path.join(proj_root)+'/api_key.json') as json_file:
    API_KEY = json.load(json_file)


class GetUserData(APIView):
    def get(self, request):
        try:
            if "id" in request.GET:
                users = User.objects.all().get(user_id=request.GET["id"], msgr_type=request.GET["msgr_type"])
            elif "username" in request.GET:
                users = User.objects.all().get(username=request.GET["username"], msgr_type=request.GET["msgr_type"])
            else:
                return Response({"success": False, "message": "Need to specify username or user_id"}, status=HTTP_200_OK)
            ser = UserSerializer(users)
            return Response({"username": ser.data['username'],
                             "wallet_address": ser.data['wallet_address'],
                             "fcm_token": ser.data['push_token']}, status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"success": False, "message": 'User does not exist'}, status=HTTP_400_BAD_REQUEST)


class LinkedUsersGetList(APIView):
    def get(self, request):
        users_list = []
        for p in User.objects.all():
            users_list.append(p.user_id)

        return Response(users_list, status=HTTP_200_OK)


class IsLinkedUser(APIView):
    def get(self, request):
        try:
            if "id" in request.GET:
                User.objects.all().get(user_id=request.GET["id"], msgr_type=request.GET["msgr_type"])
            elif "username" in request.GET:
                User.objects.all().get(username=request.GET["username"], msgr_type=request.GET["msgr_type"])
            else:
                return Response({"success": False, "message": "Need to specify username or user_id"}, status=HTTP_200_OK)
            return Response({"success": True}, status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class LinkUser(APIView):
    def post(self, request):
        ser = User()
        ser.from_json(request.data)
        if request.data.get("push_token") \
                and request.data.get("username") or request.data.get("user_id") \
                and request.data.get("msgr_type"):
            try:
                if request.data.get("user_id"):
                    user_to_update = User.objects.all().get(msgr_type=request.data.get("msgr_type"),
                                                            user_id=int(request.data.get("user_id")))
                elif request.data.get("username"):
                    user_to_update = User.objects.all().get(msgr_type=request.data.get("msgr_type"),
                                                            username=request.data.get("username"))
                else:
                    return Response({"success": False, "message": "Need to specify username or user_id"}, status=HTTP_200_OK)
                user_to_update.delete()
                ser.save()
                return Response({"success": True, "message": "User data updated"}, status=HTTP_200_OK)
            except ObjectDoesNotExist:
                ser.save()
                return Response({"success": True}, status=HTTP_200_OK)
        else:
            return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class UnlinkUser(APIView):
    def delete(self, request):
        if request.data.get("user_id") or request.data.get("username") and request.data.get("msgr_type"):
            try:
                if request.data.get("user_id"):
                    user_to_unlink = User.objects.all().get(user_id=request.GET["id"], msgr_type=request.GET["msgr_type"])
                elif request.data.get("username"):
                    user_to_unlink = User.objects.all().get(username=request.GET["username"], msgr_type=request.GET["msgr_type"])
                else:
                    return Response({"success": False, "message": "Need to specify username or user_id"},
                                    status=HTTP_200_OK)
                user_to_unlink.delete()
                return Response({"success": True, "message": "User unlinked"}, status=HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"success": False, "message": 'User does not exist'}, status=HTTP_400_BAD_REQUEST)


class NotificationManage(APIView):
    def get(self, request, message_id):
        try:
            push_req = Notification.objects.all().get(id=message_id)
            push = NotificationItemSerializer(push_req)
            return Response({"success": True, "data": push.data}, status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"success": False, "message": 'Notification does not exist'}, status=HTTP_400_BAD_REQUEST)


class NotificationSend(APIView):
    def post(self, request):
        ser = Notification()
        ser.from_json(request.data)
        if request.data.get("amount") and request.data.get("fee") \
                and request.data.get("push_type") == SILENT_PUSH_ID or request.data.get("push_type") == SHOUT_PUSH_ID \
                and request.data.get("msgr_type"):
            wallet_address = request.data.get("wallet_address")
            try:
                if request.data.get("wallet_address") and not request.data.get("send_from"):
                    receiver = '/topics/'+request.data.get("wallet_address")
                    ser.add_receiver(receiver)
                else:
                    existing_user_to = User.objects.all().get(user_id=request.data.get("send_from"),
                                                              msgr_type=request.data.get("msgr_type"))
                    send_from = UserSerializer(existing_user_to)
                    receiver = str(send_from.data['push_token'])
                try:
                    ser.save()
                    if request.data.get("push_type") == SILENT_PUSH_ID:
                        payload = {
                            "to": receiver,
                            "priority": 10,
                            "content_available": True,
                            "data": {
                                "type": "send",
                                "to": str(wallet_address),
                                "amount": str(request.data.get("amount")),
                                "fee": str(request.data.get("fee")),
                                "message_id": str(ser.get_id())
                            }
                        }
                    else:
                        payload = {
                            "to": receiver,
                            "priority": 10,
                            "notification": {
                                "title": "New transaction",
                                "body": "Reply or open app to confirm transaction",
                                "click_action": "TRANSACTION_INVITATION",
                                "sound": "default"
                            },
                            "data": {
                                "type": "send",
                                "to": str(wallet_address),
                                "amount": str(request.data.get("amount")),
                                "fee": str(request.data.get("fee")),
                                "message_id": str(ser.get_id())
                            }
                        }

                    headers = {
                        'Authorization': 'key=' + str(API_KEY),
                        'Content-Type': 'application/json',
                        'cache-control': 'no-cache'
                    }

                    requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(payload))

                    return Response({"success": True, "message_id": ser.get_id()}, status=HTTP_200_OK)
                except IntegrityError:
                    return Response({"success": False, "message": "Wrong input data"}, status=HTTP_400_BAD_REQUEST)

            except ObjectDoesNotExist:
                return Response({"success": False, "message": 'Recipient does not linked in system'},
                                status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": False, "message": 'Wrong input data'}, status=HTTP_400_BAD_REQUEST)


class NotificationUpdate(APIView):
    def put(self, request):
        item_to_update = Notification.objects.all().get(id=int(request.data.get("id")))

        if request.data.get("transaction_status"):
            item_to_update.update_transaction_status(request.data.get("transaction_status"))

        if request.data.get("push_status"):
            item_to_update.update_push_status(request.data.get("push_status"))

        try:
            item_to_update.save()
        except IntegrityError as e:
            return Response({"success": False}, status=HTTP_400_BAD_REQUEST)

        return Response({"success": True}, status=HTTP_200_OK)
