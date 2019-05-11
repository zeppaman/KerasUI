from django.shortcuts import render
from management.models import DataSet,DataSetItem
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets, mixins
from django.db import models
from api.serializers import UserSerializer, GroupSerializer, DataSetItemSerializer, DataSetSerializer,TestItemSerializer
from rest_framework.response import Response
import json
import os
from management.kmanager import KManager
import uuid
import base64
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer



class DataSetItemViewSet(viewsets.ModelViewSet):
   
    queryset = DataSetItem.objects.all()
    serializer_class = DataSetItemSerializer

class DataSetViewSet(viewsets.ModelViewSet):
   
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


class TestItemViewSet(viewsets.ViewSet):
   
    #queryset = DataSetItem.objects.all()
    serializer_class = TestItemSerializer

    def create(self, request):   
        response=  {}
        ct=request.content_type
        image_path=""
        datasetid=""

        if 'json' in ct :
            parsed=request.data
            logger.debug(parsed["dataset"])
            logger.debug(parsed["image"])

            datasetid=parsed["dataset"]
            image_path='datasets/'+str(uuid.uuid4())+'.img'
            destination = open(image_path, 'wb+')
            destination.write(base64.b64decode(parsed["image"]))
            destination.close()

        else:
            datasetid=request.data["dataset"]
            image_path = request.FILES['image'].temporary_file_path()

        logger.debug(image_path)
        logger.debug(datasetid)

        response['result']=KManager.predict(image_path, datasetid)     
         
        if 'json' in ct:
            os.remove(image_path)   
        return Response(data=response)