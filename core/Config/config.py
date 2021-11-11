from ujson import loads

class Configuration:
    def __init__(self,json_path=None):
        if json_path is not None:
            with open(json_path) as fp:
                self._json=loads(fp.read())
            self.prefix=self._json['prefix']
            self.exclude_cogs=self._json['exclude_cogs']
            self.api_router_animals=self._json['api_routers']['api_router_animals']
            self.machine_core=self._json['machine_core']
            self.token=self._json['token']
            self.ownerID=self._json['ownerID']
        else:
            self.prefix="ul!"
            self.exclude_cogs=['__pycache__','archives']
            self.api_router_animals=['cats']
            self.machine_core='perspective'
            self.token=None
            self.ownerID=765434202803929099

        self.splash='''____ _  _ _  _ _  _ _ _  _ ____ 
|__/ |  | |\ | |\ | | |\ | | __ 
|  \ |__| | \| | \| | | \| |__] '''
        self.connected_ascii=''' ____ ____ __ _ __ _ ____ ____ ___ ____ ___ 
 |___ [__] | \| | \| |=== |___  |  |=== |__>'''
