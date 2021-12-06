from nextcord.ext.commands import group,command,Cog
from nextcord.ext import tasks
from nextcord import Embed,Color
from random import choice

from typing import Optional
from asyncpraw import Reddit
from asyncio import sleep
from os import environ

class MemeFun(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.reddit=Reddit(
            client_id="ONK8_soA1vWpQqNHi0pYoQ",
            client_secret="EvumyPrt9qid67A5ogODCI1Q-Ls68g",
            password=environ['pass'],
            user_agent="ultron",
            username="ultron7506"
        )
        self.subs=['memes','dankmemes','wholesomememes','raimimemes','historymemes','okbuddyretard','comedyheaven']
        self.cats=['top','new','rising']
        self.cats_2=['gilded','controversial','hot']
        self.loaded_cat_1=False
        self.loaded_cat_2=False
        self.memes={}
        for subr in self.subs:
            self.memes.update({subr:{}})
            for cat in self.cats:
                self.memes[subr].update({cat:[]})
            for cat in self.cats_2:
                self.memes[subr].update({cat:[]})

        self.gather_meme_first.start()
        #self.gather_meme_second.start()


    @command(name="meme",aliases=['bored'])
    async def meme_command(self,ctx,cat:Optional[str]='top',sub:Optional[str]='memes'):
        if cat in ['all','cats','categories','catego','categ']:
            return await ctx.send("Current Memes Categories - {}".format(", ".join(self.cats+self.cats_2)))
        elif cat in ['channels','sources'] or cat.startswith('sub'):
            return await ctx.send("Current Subreddits - {}".format(", ".join(self.subs)))
        if (not len(self.memes[sub][cat])>0 and cat in self.cats):
            return await ctx.send("`Memes not loaded for {}'s {} memes`".format(sub,cat))
        if (not len(self.memes[sub][cat])>0 and cat in self.cats_2):
            return await ctx.send("`Memes not loaded for {}'s {} memes`".format(sub,cat))
        
        if not sub in self.subs:
            sub='memes'
        if not cat in self.cats and not cat in self.cats_2:
            cat='top'
        c=choice(self.memes[sub][cat])
        coms=c.num_comments
        auth=c.author
        #cre=c.created_utc
        t=c.title
        u=c.url
        up=c.score
        em=Embed(
            title="".join(['**__`',t,"`__**"]),
            description='```diff\n+ {} Upvotes\n+ {} Comments```'.format(up,coms),
            color=Color.from_rgb(0,0,0),
            url=u
        )
        em.set_image(url=u)
        em.set_footer(text='12k+ Memes Refreshed every 20 Minutes...')
        em.set_author(name=auth)
        await ctx.send(embed=em)

    @tasks.loop(minutes=20)
    async def gather_meme_first(self):
        for i in self.subs:
            subr=await self.reddit.subreddit(i)
            for cat in self.cats:
                x=eval("".join(['subr.',cat,'(limit=300)']))
                async for sub in x:
                    self.memes[i][cat].append(sub)
        self.loaded_cat_1=True

    @tasks.loop(minutes=20)
    async def gather_meme_second(self):
        for i in self.subs:
            subr=await self.reddit.subreddit(i)
            for cat in self.cats_2:
                async for sub in eval("".join(['subr.',cat,'(limit=300)'])):
                    self.memes[subr][cat].append(sub)
        self.loaded_cat_2=True

    @gather_meme_first.before_loop
    async def gather_meme_first_before(self):
        await self.bot.wait_until_ready()

    @gather_meme_second.before_loop
    async def gather_meme_second_before(self):
        await self.bot.wait_until_ready()
        await sleep(60)

def setup(bot):
    bot.add_cog(MemeFun(bot))