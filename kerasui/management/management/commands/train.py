#App
from django.core.management import BaseCommand
from management.models import DataSet, DataSetItem
from django.conf import settings

#AI
from keras.models import Sequential
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


from django.core.files import File


# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    IMAGE_SIZE = 256
    # Show this when the user types help
    help = "Train job"
    def add_arguments(self, parser):
        parser.add_argument('datasetid', type=int)

    
    
    




    def load_data(self, datasetid):
        self.stdout.write("loading images")
        train_data = []
        
        images = DataSetItem.objects.filter(dataset=datasetid)
        labels = [x['label'] for x in  DataSetItem.objects.values('label').distinct()]
      
        for image in images:
            self.stdout.write("Loading {0}".format(image.image))
            image_path = image.image.path
            if "DS_Store" not in image_path:           
                index=[x for x in range(len(labels)) if labels[x]==image.label]
                label = to_categorical([index,],len(labels))
                
                img = Image.open(image_path)
                img = img.convert('L')
                img = img.resize((self.IMAGE_SIZE, self.IMAGE_SIZE), Image.ANTIALIAS)
                print(np.array(img).shape)
                print(np.array(label[0]).shape)
                train_data.append([np.array(img), np.array(label[0])])
            
        return train_data

   


    # A command must define handle()
    def handle(self, *args, **options):
        self.stdout.write("Starting trainig "+str(options['datasetid']))
        datasetid=options['datasetid']
        dataset= DataSet.objects.get(pk=datasetid)
        
        training_data = self.load_data(datasetid)
      
        training_images = np.array([i[0] for i in training_data]).reshape(-1, self.IMAGE_SIZE, self.IMAGE_SIZE, 1)
        training_labels = np.array([i[1] for i in training_data])

        print(training_images.shape)
        print(training_labels.shape)

        print(training_images[0])
        print(training_labels[0])

        self.stdout.write("Creating model ")
        self.stdout.write("using process code "+dataset.process)
        
        #train
        model=Sequential()
        exec(dataset.process)
        
        labels = [x['label'] for x in  DataSetItem.objects.values('label').distinct()]

        model.add(Dense(len(labels), activation = 'softmax'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.stdout.write("Training model ")
        model.fit(training_images, training_labels, batch_size=dataset.batchSize, epochs=dataset.epochs, verbose=dataset.verbose)
        

        #save the result
        datasetToSave=DataSet.objects.get(pk=datasetid)
        datasetToSave.progress=100
        datasetToSave.model_labels=json.dumps(labels)
        
       
        temp_file_name=str(uuid.uuid4())+'.h5'
        model.save(temp_file_name)

        datasetToSave.model.save('weights.h5',File(open(temp_file_name, mode='rb')))
        
        os.remove(temp_file_name)
        datasetToSave.save()
