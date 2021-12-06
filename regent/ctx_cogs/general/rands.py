from nextcord.ext.commands import command,Cog
from random import randrange
from typing import Optional

from nextcord import Member
class Rands(Cog):
    def __init__(self,bot):
        self.bot=bot

    @command(name='random',aliases=['randnum','randint'])
    async def random_command(self,ctx,start:Optional[int]=0,end:Optional[int]=1000):
        if end>69000 or start<0 or start>end:
            return await ctx.send("`Invalid Start/End Number`")
        await ctx.send(f"`Random number from {start} to {end} := {randrange(start,end)}`")

    @command(name='howpog',aliases=['pogometer'])
    async def howpog_command(self,ctx,user:Optional[Member]=None):
        if user is None:
            user=ctx.author
        
        av=randrange(4,randrange(15,30))
        rv=randrange(42,69)-randrange(7 if 7<len(user.name) else 0,len(user.name))
        tv=av+rv+randrange(0,100)/100
        if tv>100:
            tv=100
        await ctx.send(f"`The user {user.display_name} is {round(tv*10000)/10000}% pog`")

    
def setup(bot):
    bot.add_cog(Rands(bot))