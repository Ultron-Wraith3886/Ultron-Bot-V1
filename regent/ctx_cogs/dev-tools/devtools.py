from nextcord.ext.commands import Cog,group
from nextcord import Embed,Color
from typing import Optional
import hashlib

class DEVTOOLS(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.hashes=[]
        self.hashes.extend(list(hashlib.algorithms_available))

    @group(name='devtools',aliases=['dt'],invoke_without_command=True)
    async def devtools_grp(self,ctx):
        await ctx.send("INDEV DEVTOOLS GRP")

    @devtools_grp.command(name='hash')
    async def hash_command(self,ctx,mode:Optional[str]='sha256',*,inps:Optional[str]='hello world'):
        try:
            r=eval("".join(['hashlib.',mode,'(',"b'",inps,"'",')','.hexdigest()']))
        except Exception as e:
            print(e)
            r="Couldn't Hash in {}".format(mode)
        em=Embed(
            title='**`{} Hash`**'.format(mode.upper()),
            description="```\"{}\"s {} Hash\n{}```".format(inps,mode,r),
            color=Color.from_rgb(0,0,0)
        )
        await ctx.send(embed=em)
    
def setup(bot):
    bot.add_cog(DEVTOOLS(bot))