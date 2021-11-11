import os,json
from pathlib import Path
import grequests as requests
from typing import Optional

from datetime import datetime as dt

import pokebase as pb

class CogRouter:
    def __init__(self,exclude_cogs=['__pycache__']):
        self.cogs=[]
        self.cog_directory=["regent/ctx_cogs/*","regent.ctx_cogs"]
        self.cog_names=[p.stem for p in Path(".").glob(self.cog_directory[0])]
        for name in exclude_cogs:
            del self.cog_names[self.cog_names.index(name)]
    
    def returnRoutes(self):
        for entry in self.cog_names:
            for pyfile in os.listdir(f'{self.cog_directory[0][:-1]}/{entry}'):
                if pyfile != '__pycache__':
                    self.cogs.append(f'{self.cog_directory[1]}.{entry}.{pyfile[:-3]}')
        return self.cogs
    
class APIRouter_REST:
    def __init__(self,apis='all'):
        self.api_collection={
            "axolotl":{
                "url":"https://axoltlapi.herokuapp.com/"
            },
            "dogs":{
                "url":"https://dog.ceo/api/breeds/image/random",
                "meth":"message"
            },
            "cats":{
                "url":"https://thatcopy.pw/catapi/rest/",
                "meth":'webpurl'
            },
            "foxes":{
                "url":'https://randomfox.ca/floof/',
                'meth':'image'
            },
            "ducks":{
                "url":"https://random-d.uk/api/random"
            },
            "dog-facts":{
                "url":"http://dog-api.kinduff.com/api/facts",
                "meth":"facts"
            }
        }
        self.api_allowed={}
        self.api_names=[]
        if apis == 'all':
            self.api_allowed=self.api_collection
            for api in self.api_allowed:
                api=str(api)
                api_name=list(api)
                api_name[0]=api_name[0].upper()
                self.api_names.append("".join(api_name))
        else:
            for api in apis:
                self.api_allowed.update({api:self.api_collection[api]})
                api_name=list(api)
                api_name[0]=api_name[0].upper()
                self.api_names.append("".join(api_name))
        
        del self.api_names[self.api_names.index('Dog-facts')]

        
    async def requestRoute(self,api_name:str='axolotl',extra_param=''):
        try:
            if 'meth' in self.api_allowed[api_name].keys():
                meth=self.api_allowed[api_name]['meth']
            else:
                meth='url'
            return json.loads(requests.map([requests.get(self.api_allowed[api_name]['url']+extra_param)])[0].content.decode('utf-8')),meth
        except:
            return None,None

class APIRouter_Anime:
    def __init__(self,apis='all'):
        self.api_collection={
            "quotes":{
                "url":"https://animechan.vercel.app/api/random",
                'meth':'quote'
            },
            "facts":{
                "url":"https://anime-facts-rest-api.herokuapp.com/api/v1"
            }
        }
        self.api_allowed={}
        self.api_names=[]
        if apis == 'all':
            self.api_allowed=self.api_collection
            for api in self.api_allowed:
                api=str(api)
                api_name=list(api)
                api_name[0]=api_name[0].upper()
                self.api_names.append("".join(api_name))
        else:
            for api in apis:
                self.api_allowed.update({api:self.api_collection[api]})
                api_name=list(api)
                api_name[0]=api_name[0].upper()
                self.api_names.append("".join(api_name))
    async def requestRoute(self,api_name:str='quote',extra_param=''):
        try:
            if 'meth' in self.api_allowed[api_name].keys():
                meth=self.api_allowed[api_name]['meth']
            else:
                meth='url'
            return json.loads(requests.map([requests.get(self.api_allowed[api_name]['url']+extra_param)])[0].content.decode('utf-8')),meth
        except Exception as e:
            print(e)
            return None,None


             
            
