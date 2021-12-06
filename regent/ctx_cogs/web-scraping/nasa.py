from nextcord.ext.commands import command,Cog,group,is_owner
from nextcord import Embed, Color
from time import perf_counter
from aasr.Requests import AAS_URLInterface
from nextcord.ext import tasks
import random
from typing import Optional
from os import environ
import gc

class Nasa(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.nasa_url='https://api.nasa.gov'
        self.apod='/planetary/apod?api_key=$api'
        self.epic=['/EPIC/api/natural/images','/EPIC/archive/natural/%Y/%M/%D/png/$image']
        self.rover='/mars-photos/api/v1/rovers/$rover/photos?sol=$sol&page=$page&api_key=$api'
        self.rover_sols={'curiosity':3300,'opportunity':5000,'spirit':2000}
        self.rovers=['opportunity','curiosity','spirit']
        self.api_key=environ['nasa']
        self.rover_m=0
        self.data={'_apod':{},'curiosity':{},'spirit':{},'opportunity':{}}

        self.search_url='https://images-api.nasa.gov/search?q=$query'
        self.asset_url='https://images-assets.nasa.gov/image/$id/$id~orig.jpg'

        self.requests_peer_0=AAS_URLInterface(request_limit_per_host=169)
        self.requests_peer_1=AAS_URLInterface(request_limit_per_host=169)
        self.requests_peer_2=AAS_URLInterface(request_limit_per_host=169)

        self.ac,self.rc=False,False
        self.session_management.start()
        self.rover_collect.start()
        self.apod_collect.start()

    @tasks.loop(minutes=30)
    async def session_management(self):
        await self.requests_peer_0.close_session()
        await self.requests_peer_1.close_session()
        await self.requests_peer_2.close_session()
        self.requests_peer_0=AAS_URLInterface(request_limit_per_host=169)
        self.requests_peer_1=AAS_URLInterface(request_limit_per_host=169)
        self.requests_peer_2=AAS_URLInterface(request_limit_per_host=169)

    @command(name='testreq',aliases=['tr'])
    @is_owner()
    async def tr_command(self,ctx,url:str,decoding:str='utf-8'):
        e=AAS_URLInterface(1)
        r=await e.map([await e.get(url,decoding=decoding)],load=True)
        await e.close_session()
        await ctx.send(str(r[0]))

    @command(name='reqspeed',aliases=['rp'])
    @is_owner()
    async def reqs(self,ctx,num:int=60,limit:int=60):
        u=['https://jsonplaceholder.typicode.com/todos/']*num
        u=[v+str(i+1) for i,v in enumerate(u)]
        r=AAS_URLInterface(limit)
        x=perf_counter()
        f=await r.map([await r.get(url) for url in u])
        r.refresh()
        await ctx.send("Did {} Requests with AASR in {}s || Limit - {}".format(str(num),str(round((perf_counter()-x)*100)/100),limit))
        await r.close_session()
        gc.collect()
        
        
    @tasks.loop(hours=1,minutes=30)
    async def rover_collect(self):
        req=[]
        for rover in self.rovers:
            page=1
            sol=random.randrange(1,self.rover_sols[rover])
            url=self.nasa_url+self.rover.replace('$rover',rover)
            url=url.replace('$sol',str(sol))
            url=url.replace('$page',str(page))
            url=url.replace('$api',environ['nasa'])
            req.append(await self.requests_peer_0.get(url=url,decoding='utf-8'))
        r=await self.requests_peer_0.map(req,load=True)
        self.requests_peer_0.refresh()
        for indx,rover in enumerate(r):
            i=rover['photos'][0]['rover']['name'].lower() if len(rover['photos'])>0 else 'placeholder'
            self.data[i]=rover
        self.rc=True

    @tasks.loop(hours=24)
    async def apod_collect(self):
        f=await self.requests_peer_1.map([await self.requests_peer_1.get(self.nasa_url+self.apod.replace('$api',environ['nasa']))],load=True)
        self.data['_apod']=f
        self.requests_peer_1.refresh()
        self.ac=True

    @apod_collect.before_loop
    async def acbl(self):
        await self.bot.wait_until_ready()

    @rover_collect.before_loop
    async def rcbl(self):
        await self.bot.wait_until_ready()
        
    @group(name='nasa',invoke_without_command=True)
    async def nasa_grp(self,ctx,query:Optional[str]='apollo'):
        return await ctx.send("Nasa GRP INDEV")
        u=self.search_url.replace('$query',query)
        print(u)
        r=await self.requests_peer_2.map([await self.requests_peer_2.get(u)])
        print(r)
        c=r[0]['collection']['items'][0]['data'][0]
        i=self.asset_url.replace('$id',c['nasa_id'])
        em=Embed(
            title='**`{}`**'.format(c['title']),
            description='```{}```'.format(c['description'].split('.',3)[:2].replace('.','',1)),
            color=Color.from_rgb(0,0,0),
        )
        em.set_image(url=i)
        await ctx.send(em)


    @nasa_grp.command(name='rover')
    async def nasa_rover(self,ctx,rover:Optional[str]='random'):
        if not self.rc:
            return await ctx.send("Rover Images Not Loaded Yet...")
        if rover == 'random':
            rover=random.choice(self.rovers)
        if rover not in self.rovers and rover != 'random':
            return await ctx.send("Unidentified Rover Name")
        else:
            rover=self.data[rover]
        if len(rover['photos'][0])==0:
            return await ctx.send("Couldn't find Images for {} Rover".format(rover.capitalize()))

        img=random.choice(rover['photos'])
        em=Embed(
            title='**`Nasa Mars {} Rover Imagery || Status - {}`**'.format(img['rover']['name'],img['rover']['status']),
            description='**`Image ID - {} || Sols Refreshed Every 1.5 Hours`**'.format(img['id']),
            color=Color.from_rgb(0,0,0),
            url=img['img_src']
        )
        em.add_field(name="**`Sol - {}`**".format(img['sol']),value="_ _",inline=False)
        em.set_footer(text='Taken on {}'.format(img['earth_date']))
        em.set_author(name='{} - {}'.format(img['camera']['full_name'],img['camera']['name']),icon_url=img['img_src'])
        em.set_image(url=img['img_src'])
        await ctx.send(embed=em)

    @nasa_grp.command(name='apod')
    async def nasa_apod(self,ctx):
        if not self.ac:
            return await ctx.send("APOD Not Loaded yet...")
        d=self.data['_apod'][0]
        em=Embed(
            title='**`Nasa APOD - Astronomy Picture of the Day`**',
            description='```{}```'.format(".".join(d['explanation'].split('.',3)[:2])).replace('.','',1),
            color=Color.from_rgb(0,0,0),
            url=d['url']
        )
        em.set_image(url=d['hdurl'])
        em.add_field(name='**`{}`**'.format(d['title']),value="_ _",inline=False)
        em.set_footer(text='Date - {}'.format(d['date']))
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Nasa(bot))