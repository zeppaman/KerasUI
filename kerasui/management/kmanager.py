from django.contrib import admin
from management.models import DataSet,DataSetItem
from django import forms
from django.db import models
from django.conf import settings
from django.core.management import call_command
import threading
from django.core.files.storage import FileSystemStorage
import zipfile
import os
from os import listdir
from os.path import isfile, join
import shutil
from django.core.files import File
from django.urls import path
from django.core.files import File

from keras.models import Sequential,load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from PIL import Image
from random import shuffle, choice
import numpy as np
import os
from keras.utils import to_categorical
import tempfile
import uuid
import json
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)
  
class KManager:
  

    @staticmethod
    def get_image_size():
        return 256

    @staticmethod
    def predict(image_path,datasetid):
        logger.info("predicting "+image_path+" "+datasetid)
        dataset=DataSet.objects.get(pk=datasetid)
        modelpath=dataset.model.path        
        logger.info("model path "+modelpath)

        model=load_model(modelpath)
        labels=json.loads(dataset.model_labels)
        
        img = Image.open(image_path)
        img = img.convert('L')
        img = img.resize((256, 256), Image.ANTIALIAS)

        result= model.predict(np.array(img).reshape(-1,256,256, 1))
        max=result[0]
        idx=0
        for i in range(1,len(result)):
            if max<result[i]:
                max=result[i]
                idx=i

        logger.info(result[idx])
        logger.info(labels[idx])
        return labels[idx]