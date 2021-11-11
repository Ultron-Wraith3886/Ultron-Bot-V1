import ujson

class Guilds:
    def __init__(self,filepath="database/guilds_json.json"):
        self.fp=filepath
        with open(self.fp,'r') as fp:
            self.dict=ujson.loads(fp.read())

    #Normal Functions - Daniel
        
    def addGuild(self,id,extra_params=None):
        self.dict.update({
            id:{
                "prefix":None,
                "muted_role":None,
                "log_channel":None,
                "minute-mutes":{},
                "hour-mutes":{},
                "day-mutes":{},
                "undefined-mutes":{}
            }
        })
        if extra_params is not None:
            self.dict[id].update(extra_params)
    
    def removeGuild(self,id):
        self.dict.pop(id)
    
    def save(self):
        with open(self.fp,'w') as fp:
            fp.write(ujson.dumps(self.dict,indent=4))
        self.dict=ujson.loads(open(self.fp).read())
    
    def addAttrGuild(self,id,attrs:dict):
        self.dict[id].update(attrs)

    def setMutedRole(self,id,role=None):
        id=str(id)
        if role is None:
            self.dict[id]['muted_role']=None
        else:
            self.dict[id]['muted_role']=role
    
    def addLogChannel(self,id,channelid):
        self.dict[str(id)]['log_channel']=channelid

    def removeLogChannel(self,id):
        id=str(id)
        self.dict[id]['log_channel']=None 

    def getMutedRole(self,id):
        return self.dict[str(id)]['muted_role']
    
    def getLogChannel(self,id):
        return self.dict[str(id)]['log_channel']
    
    def getPrefix(self,id):
        id=str(id)
        return self.dict[id]['prefix']
    
    def checkForGuild(self,id):
        return id in self.dict
    
    def setPrefix(self,id,prefix='ul'):
        id=str(id)
        self.dict[id]['prefix']=prefix
    
    def addMute(self,guildID,targetID,roleID,end_time,category):
        guildID=str(guildID)
        self.dict[guildID][category].update({
            targetID:{
                'end_time':end_time,
                'roles':roleID
            }
        })

    def removeMute(self,guildID,targetID,cat):
        self.dict
        self.dict[str(guildID)][cat].pop(targetID)
    
    def setMuteRole(self,id,role):
        self.dict[id]['muted_role']=role
    
    def getRoleID(self,id,target_id,cat):
        self.dict
        return self.dict[str(id)][cat][target_id]['roles']
    
    def getMutes(self,id,cat):
        return self.dict[str(id)][cat]
    
    def getMute(self,id,MemberID,cat):
        return self.dict[str(id)][cat][MemberID]

    def ismuted(self,id,mid):
        for cat in ['undefined-mutes','minute-mutes','hour-mutes','day-mutes']:
            if mid in self.dict[str(id)][cat].keys():
                return True

        return False