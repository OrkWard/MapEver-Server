from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse


@api_view(['PUT'])
def overlay(request):
    return HttpResponse('overlay finish!' + str(request.data))