from nextcord.ext.commands import group,command,Cog
from nextcord.ext import tasks
from nextcord import Embed,Color
from random import choice

from typing import Optional
from praw 
from asyncio import sleep
from os import environ

class MemeFun(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.reddit=Reddit(
            client_id="ONK8_soA1vWpQqNHi0pYoQ",
            client_secret="	EvumyPrt9qid67A5ogODCI1Q-Ls68g",
            password=environ['pass'],
            user_agent="ultron",
            username="ultron7506"
        )
        self.subs=['memes','dankmemes','wholesomememes','raimimemes','historymemes','okbuddyretard','comedyheaven']
        self.cats=['top','new','rising']
        self.cats_2=['gilded','controversial','hot']
        self.memes={}
        for subr in self.subs:
            self.memes.update({subr:{}})
            for cat in self.cats:
                self.memes[subr].update({cat:[]})
            for cat in self.cats_2:
                self.memes[subr].update({cat:[]})

        self.gather_meme_first.start()
        self.gather_meme_second.start()

    @command(name="meme",aliases=['bored'])
    async def meme_command(self,ctx,cat:Optional[str]='top',sub:Optional[str]='memes'):
        if not sub in self.subs:
            sub='memes'
        
        if not cat in self.cats and not cat in self.cats_2:
            cat='top'

        c=choice(self.memes[sub][cat])
        coms=c.num_comments
        auth=c.author
        cre=c.created_at
        t=c.title
        u=c.url
        up=c.score
        em=Embed(
            title="".join(['**__`',t,"`__**"]),
            color=Color.from_rgb(0,0,0),
            url=u
        )
        em.set_image(url=u)
        em.set_footer(text='`Created at {}`'.format(cre))
        em.set_author(name=auth)
        em.add_field(name="_ _",value="⬆️ {} || 💬 {}".format(up,coms))

    @tasks.loop(minutes=1)
    async def gather_meme_first(self):
        for i in self.subs:
            subr=await self.reddit.subreddit(i)
            for cat in self.cats:
                for sub in eval("".join(['subr.',cat,'(limit=99)'])):
                    self.memes[subr][cat]
                    print("added ",sub)

    @tasks.loop(minutes=1)
    async def gather_meme_second(self):
        for i in self.subs:
            subr=await self.reddit.subreddit(i)
            for cat in self.cats_2:
                for sub in eval("".join(['subr.',cat,'(limit=99)'])):
                    self.memes[subr][cat].append(sub)

    @gather_meme_first.before_loop
    async def gather_meme_first_before(self):
        await self.bot.wait_until_ready()

    @gather_meme_second.before_loop
    async def gather_meme_second_before(self):
        await self.bot.wait_until_ready()
        await sleep(60)

def setup(bot):
    bot.add_cog(MemeFun(bot))