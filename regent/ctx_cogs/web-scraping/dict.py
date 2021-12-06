from nextcord.ext.commands import Cog,group
from nextcord import Embed,Color
from PyDictionary import PyDictionary
from typing import Optional
import wikipedia

class Definitions(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.d=PyDictionary()

    @group(name='dictionary',aliases=['dict','urban','meaning'],invoke_without_command=True)
    async def dict_grp(self,ctx):
        await ctx.send("Dict Command")

    @dict_grp.command(name='define',aliases=['meaning'])
    async def define_command(self,ctx,*,inp:Optional[str]='Life'):
        m=self.d.meaning(inp)
        if m is None:
            return await ctx.send("`No Meanings for that`")
        em=Embed(
            title='**`Meaning of {}`**'.format(inp),
            description='**`Detected {}`**'.format(", ".join(list(m.keys())).replace(',','',0)),
            color=Color.from_rgb(0,0,0)
        )
        t=list(m.keys())
        tries=3
        f=[('**{}**'.format(n), '```{}```'.format("$place".join([meaning.capitalize() for indx,meaning in enumerate(m[n]) if indx+1<tries]).replace('$place','.\n',-1)),False) for n in t]
        for name,value,inline in f:
            em.add_field(name=name,value=value,inline=inline)
        await ctx.send(embed=em)

    @group(name='wiki',aliases=['wikipedia','mediawiki'],invoke_without_command=True)
    async def wiki_grp(self,ctx):
        await ctx.send("Wikipedia INDEV COMMANDS")

    @wiki_grp.command(name='search',aliases=['srch','find'])
    async def search_query(self,ctx,results:Optional[int]=5,*,inp:Optional[str]='Discord'):
        if results>16:
            return await ctx.send("Cannot show more than 16 results")
        r=wikipedia.search(inp,results=results,suggestion=False)
        em=Embed(
            title='**`Wiki Search Results for {}`**'.format(inp),
            description='```{}```'.format(",$placeholder".join(r).replace('$placeholder','\n')),
            color=Color.from_rgb(0,0,0)
        )
        await ctx.send(embed=em)

    @wiki_grp.command(name='summary',aliases=['define','meaning'])
    async def summary_wiki(self,ctx,*,title:Optional[str]='Discord'):
        try:
            r=wikipedia.summary(title, sentences=3, auto_suggest=False)
            em=Embed(
                title='**`Results for {}`**'.format(title),
                description='```{}```'.format(r),
                color=Color.from_rgb(0,0,0)
            )
            await ctx.send(embed=em)
        except wikipedia.exceptions.DisambiguationError as e:
            opt=e.options
            em=Embed(
                title='**`No Summaries Found`**',
                description='**`Here are a few query suggestions`** - \n```{}```'.format(",\n".join([f for indx,f in enumerate(opt) if indx<5])),
            )
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Definitions(bot))