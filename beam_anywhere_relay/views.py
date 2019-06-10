from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from django.views.generic import TemplateView
import json
import os

from django.http import JsonResponse


class AppleAssociation(APIView):
    def get(self, request):
        settings_dir = os.path.dirname(__file__)
        proj_root = os.path.abspath(os.path.dirname(settings_dir))
        with open(os.path.join(proj_root)+'/apple-app-site-association.json') as json_file:
            data = json.load(json_file)
        return JsonResponse(data)


class LinkUser(APIView):
    def get(self, request):
        return Response(status=HTTP_200_OK)


class HomePageView(TemplateView):
    template_name = 'home.html'
