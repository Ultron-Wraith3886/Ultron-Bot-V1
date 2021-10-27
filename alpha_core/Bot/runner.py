#Dependancies
import os
import nextcord as discord
from pathlib import Path
from nextcord.ext import commands

from database import database

#MODELS
#from core.Models.UltronAI.Layers.directProfanity import profanityDirect
from alpha_core.Resources.UltronAI.Layers.profanityAI import bertia
from delta_core.Routers import router
from alpha_core.Resources.Config import config

#Bot Config
''''
bot = commands.Bot(command_prefix='.')
intents = discord.Intents.all()
bot.remove_command("help")'''

class Bot(commands.AutoShardedBot):
    def __init__(self):
        self._configurator=config.Configuration()
        print(self._configurator.splash)

        self.db=database.Guilds()
        self.prefix=self._configurator.prefix

        self._cog_router=router.CogRouter(self._configurator.exclude_cogs)
        self._api_router_animals=router.APIRouter_Animals(['cats'])
        self._owner_id=self._configurator.ownerID

        self._cogs=self._cog_router.returnRoutes()
        self.shard_count=1
        Intents=discord.Intents.all()
        super().__init__(command_prefix=self.prefix,intents=Intents ,case_insensitive=True)
        self.model=bertia.machineCore(self._configurator.machine_core)
        self.model.initiate()

    def setup(self):
        print("\n\n---Loading Extensions and Commands---\n")
        for cogs in self._cogs:
            try:
                self.load_extension(cogs)
                print(f"--Loaded {cogs}.py--")
            except:
                print(f"--Couldn't load {cogs}.py--")
        print("\n---Loaded all Extensions---\n\n")
        
    def run(self):
        self.setup()

        TOKEN=os.environ['ULTRON_TOKEN']
        print("Executing RUN Procedure")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing Connection")
        await super().close()

    async def close(self):
        print("Terminating on KeyPress")
        await self.shutdown()

    async def on_connect(self):
        print(self._configurator.connected_ascii)

    async def on_resumed(self):
        print("RESUMED")

    async def on_disconnect(self):
        print("DISCONNECTED")

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print('_________________________________________________ ')
        print(''' _     _        _______  ______  _____  __   _
 |     | |         |    |_____/ |     | | \  |
 |_____| |_____    |    |    \_ |_____| |  \_|''')
        print('_________________________________________________ ')
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                    name='the Universe'))
        print('Ultron™ | Made and Maintained by Wraith#3886')
        print('_________________________________________________')

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(".")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, ctx):
        ctx=await self.get_context(ctx)
        if not ctx.author.bot:
            if (ctx.author != ctx.guild.owner or ctx.author.id==self._owner_id) and not(ctx.message.content.startswith(self.prefix)):
                req=self.model.think(ctx.message.content)
            else:
                req=0
            if req>88:
                em=discord.Embed(
                    title="**`Message Violated and Tried to bypass Moderation through Toxicity`**",
                    description=f"`{ctx.message.content} violated at a score of {req}%`",
                    color=discord.Color.from_rgb(0,0,0),
                    url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                )
                em.set_author(name=ctx.author.display_name,url=ctx.author.display_avatar.url)
                em.set_footer(text="I see all")
                await ctx.delete()
                await ctx.channel.send(embed=em)
            await self.process_commands(ctx.message)
    
    async def _encrypt(self,string:str):
        return string
    async def _decrypt(self,bytesstr):
        return bytesstr
#Startup Log
'''
@bot.event
async def on_ready():
    


#Keeping the bot Running

'''

