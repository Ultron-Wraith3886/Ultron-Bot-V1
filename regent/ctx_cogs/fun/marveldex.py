import nextcord as discord
from nextcord.ext import commands,tasks
from nextcord.ext.commands import Cog, group

from nextcord import Embed
from typing import Optional

from difflib import get_close_matches

class MarveldexFun(Cog):
    def __init__(self,bot):
        self.bot=bot

    @tasks.loop(minutes=30)
    async def marvel_dex_looper(self):
        pass
        header="""
        --hi--
        """.format()
    

def setup(bot):
    bot.add_cog(MarveldexFun(bot))