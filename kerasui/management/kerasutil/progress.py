from keras.callbacks import ProgbarLogger,Callback
import math
from management.models import DataSet, DataSetItem
from django.conf import settings
from django.db import models
import tensorflow
import threading

class ProgressLogger(Callback):
    def __init__(self, dataset_id):
        Callback.__init__(self)
        self.seen = 0
        self.dataset_id = dataset_id
        
        self.samples=1000
        self.oldperc=0
       # print('inited '+self.samples+' '+self.dataset_id)
    def on_train_begin(self, batch, logs={}):
        #  print(batch)
        #  print(logs.items)
        #  print(self.params['samples'])
        self.samples=self.params['samples']
        self.epoch=self.params['epochs']
        self.total=self.samples* self.epoch        
        ds=DataSet.objects.get(pk=self.dataset_id)
        ds.progress=0
        ds.save()


    def on_batch_end(self, batch, logs={}):
        self.seen += logs.get('size', 0)
        if self.samples>0:
            perc=math.ceil(self.seen*100/self.total)
            print('>completed '+str(self.seen)+' of '+str(self.total)+":"+str(perc))
            if(self.oldperc!=perc):
                self.oldperc=perc
                ds=DataSet.objects.get(pk=self.dataset_id)
                ds.progress=perc
                ds.save()
                


