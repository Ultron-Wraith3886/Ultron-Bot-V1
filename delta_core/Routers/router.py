import os 
from pathlib import Path
import grequests as requests

class CogRouter:
    def __init__(self,exclude_cogs=['__pycache__']):
        self.cogs=[]
        self.cog_directory=["delta_core/ctx_cogs/*","delta_core.ctx_cogs"]
        self.cog_names=[p.stem for p in Path(".").glob(self.cog_directory[0])]
        for name in exclude_cogs:
            del self.cog_names[self.cog_names.index(name)]
    
    def returnRoutes(self):
        for entry in self.cog_names:
            for pyfile in os.listdir(f'{self.cog_directory[0][:-1]}/{entry}'):
                if pyfile != '__pycache__':
                    self.cogs.append(f'{self.cog_directory[1]}.{entry}.{pyfile[:-3]}')
        return self.cogs

class APIRouter_Animals:
    def __init__(self,apis:list=['cats']):
        self.api_collection={
            "cats":{
                "url":"https://thatcopy.pw/catapi/rest/",
                "heads":'webpurl'
            }
        }
        self.api_allowed={}
        for api in apis:
            self.api_allowed.update({api:self.api_collection[api]})
    
    async def requestRoute(self,api_name:str):
        heads=self.api_allowed[api_name]['heads']
        print(requests.get(self.api_allowed[api_name]['url']).json()[heads])

    async def getAPIs(self,api_list:list):
        returns=[]
        for api in api_list:
            if api in self.api_allowed:
                returns.append(self.api_allowed[api])
        return returns
    


    
