from os import system,chdir,environ
#import tensorflow as tf
#import tensorflow_text as text 
#import tensorflow_decision_forests as tfdf

import numpy as detoxify

#import perspective
from googleapiclient import discovery
import json

args=['TOXICITY']

class machineCore:
    def __init__(self,type=None,version='1'):
        self.type=type

        self.version=version
        self.router=routerCore(0)
        self.initialized=False
        self.model=None;


    def initiate(self):
        if self.type is None:
            return
        #Tensorflow
        if self.type=='tensorflow':
            system('ls')
            #model=tf.keras.models.load_model(f'core/Resources/UltronAI/Layers/profanityAI/UltronProfNewModel/',compile=True)
     
        #Detoxify
        elif self.type=="detoxify-original" or self.type=="d.og":
            model=detoxify.Detoxify('original')
        elif self.type=="detoxify-unbiased" or self.type=="d.ub":
            model=detoxify.Detoxify('unbiased')
        elif self.type=="detoxify-multilingual" or self.type=="d.ul" or self.type=="d.ml":
            model=detoxify.Detoxify('multilingual')

        #Huggingface 
        #There is none 

        #perspective
        elif self.type=="perspective":
            class Model:
                def __init__(self):
                    self.type='perspective'
                    self.client=discovery.build(
                      "commentanalyzer",
                      "v1alpha1",
                      developerKey=environ['persapi'],
                      discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                    static_discovery=False
                    )
                def predict(self,param):
                    ar={'comment': {'text':param},
                        'requestedAttributes':{'TOXICITY':{}}
                    }
                    return self.client.comments().analyze(body=ar).execute()
            self.model=Model()
            return
        
        self.initialized=True
        self.model=model

    def think(self,param):
        if self.type=="perspective":
         return round((self.model.predict(param)['attributeScores']['TOXICITY']['spanScores'][0]['score']['value']*10000))/100
        else:
            return 
   
class routerCore:
    def __init__(self,num,type='machine'):
        self.shard=num
        self.type=type

    async def getRoute(self):
        pass

    async def listRoutes(self):
        pass
    
    async def renderlist(self,ls:list):
        pass
