from antispam import AntiSpamHandler
from antispam.plugins import AntiSpamTracker, Options

import nextcord
from nextcord import Color
from nextcord.ext import commands

from nextcord.ext.commands import Cog

class AntiSpam(Cog):
    def __init__(self,bot,opts='Options(no_punish=True)',tracking=True,handler_opts:dict={"punish_req":5,"templating":True}):
        self.opts=opts
        self.bot=bot
        if handler_opts['templating']:
            temp={
                "title":"**`$USERNAME is being warned for Spam`**",
                "description":"You were warned for Spamming the Chats in $GUILDNAME",
                "timestamp":True,
                "color":Color.from_rgb(0,0,0),
                "author":{"name":"$GUILDNAME","icon_url":"$BOTAVATAR"},
                "fields":{
                    {"name":"**__`Spam Warns for $USERNAME`__**","value":"$WARNCOUNT","inline":False},
                    {"name":"**__`Kick-Count for $USERNAME as of Spamming`__**","value":"$KICKCOUNT","inline":False}
                }
            }
        if opts!='':
            if handler_opts['templating']:
                lis=[char for char in opts]
                opts=lis.insert(lis.index(")")-1,[char for char in [',guild_warn_message=temp']])
                opts="".join(opts)
                print(opts)
                opts=eval(opts)
        self.bot.handler=AntiSpamHandler(bot,options=opts)

        if tracking:
            self.bot.tracker=AntiSpamTracker(self.bot.handler,handler_opts['punish_req'])
            self.bot.handler.register_extension(self.bot.tracker)
        
            

    @Cog.listener()
    async def on_ready(self):
        print("-- Anti Spam Ready --")
    
    @Cog.listener()
    async def on_message(self,msg):
        await self.bot.handler.propagate(msg)
        
def setup(bot):
    bot.add_cog(AntiSpam(bot))


    

            