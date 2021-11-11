import nextcord as discord
from nextcord.ext import commands
from nextcord.ext.commands import Cog

from nextcord import Embed,Color

from typing import Optional
from difflib import get_close_matches
import random

class FunCommands(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.api_names=self.bot._api_router.api_names

    @commands.command(name="image",aliases=['img','sendmeaveryniceimageplsimverybored'])
    async def image_command(self,ctx,*,tag:Optional[str]=''):
        tag=tag.lower()
        if tag == '':
            embed=Embed(
                title='**All Image Tags**',
                color=Color.from_rgb(0,0,0)
            )
            fields=[api for api in self.api_names]
            for indx,name in enumerate(fields):
                embed.add_field(name=name,value="_ _")

        elif tag.startswith('search'):
            tag=tag.split()
            del tag[0]
            embed=Embed(
                title="**6 Top Image Tags related to the Query**",
                color=Color.from_rgb(0,0,0)
            )
            fields=get_close_matches(" ".join(tag),self.api_names,6,0.25)
            embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.display_avatar.url)
            for indx,name in enumerate(fields):
                embed.add_field(name=f"{indx+1} - {name}",value="_ _",inline=False)

        else:
            tag=tag.split()
            closest=get_close_matches(" ".join(tag),self.api_names,cutoff=0.4)
            if len(closest)==0:
                closest=' '
            else:
                closest=closest[0]
            resp,meth=await self.bot._api_router.requestRoute(api_name=closest.lower())
            if resp is not None:
                embed=Embed(
                    title="**Image Result!**",
                    color=Color.from_rgb(0,0,0)
                )
                embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.display_avatar.url)
                embed.set_image(url=resp[meth])
                if closest == 'Dogs':
                    factresp,meth=await self.bot._api_router.requestRoute(api_name='dog-facts')
                else:
                    factresp=None
                if factresp is not None:
                    if type(factresp[meth]) is list:
                        factresp[meth]=factresp[meth][0]  
                    embed.add_field(name=f"**Fact** - **`{factresp[meth]}`**",value="_ _",inline=False)
                else:
                    if meth in resp.keys():
                        embed.add_field(name=f"**Fact** - **`{resp['facts']}`**",value="_ _",inline=False)
            else:
                return await ctx.send(f"`Thats an Unrecognized Image Tag!, consider doing - [{self.bot.prefix}image ] to get all the tags or do [{self.bot.prefix}image search tag-name ] to get related tags your tag-name!`")
            
        await ctx.send(embed=embed)
        
    @commands.command(name="anime",aliases=['animetag'])
    async def anime_command(self,ctx,*,tag:Optional[str]=''):
        tag=tag.lower()
        if tag=='':
            embed=Embed(
                title="**All Anime Tags**",
                color=Color.from_rgb(0,0,0)
            )
            embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.display_avatar.url)
            fields=[tag for tag in self.bot._api_router_anime.api_names]
            for index,name in enumerate(fields):
                embed.add_field(name=name,value="_ _")
        
        elif tag=='quote':
            resp,meth=await self.bot._api_router_anime.requestRoute('quotes')
            embed=Embed(
                            title="**Quote from Anime**",
                            color=Color.from_rgb(0,0,0)
                        )
            embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.display_avatar.url)
            resp[meth]=resp[meth].replace(' s ',"'s ")
            embed.add_field(name=f"**__{resp['anime']}__**",value=f"**`\"{resp[meth]}\"`** - `{resp['character']}`")

        elif tag.startswith('fact'):
            resp1,_=await self.bot._api_router_anime.requestRoute('facts')
            random_anime=random.choice(resp1['data'])['anime_name']
            resp2,_=await self.bot._api_router_anime.requestRoute('facts',extra_param=f'/{random_anime}')
            fact=random.choice(resp2['data'])['fact']
            img=resp2['img']
            fact=fact.replace(' s ',"'s ")
            embed=Embed(
                title=f"**Anime Fact from [{random_anime}]**",
                color=Color.from_rgb(0,0,0)
            )
            embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.display_avatar.url)
            embed.add_field(name=f"**Fact** - {fact}",value="_ _")
            embed.set_image(url=img)

        else:
            embed=None

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunCommands(bot))