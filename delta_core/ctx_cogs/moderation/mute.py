import nextcord as discord
from nextcord.ext import commands,tasks
from asyncio import sleep

import datetime
from typing import Optional
from datetime import datetime as dt

#Classes
from nextcord import Embed, Member

from nextcord.utils import sleep_until
from nextcord import HTTPException, Forbidden
from nextcord.ext.commands import Cog, Greedy
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands import MissingRequiredArgument, BadArgument, has_permissions, bot_has_permissions, CheckFailure

class Mute(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.db=self.bot.db

        # Mute Checkers
        self.minute_mute_checker.start()
        self.hour_mute_checker.start()
        self.day_mute_checker.start()

        # File Saver
        self.save_file.start()
    
    async def cunm(self,channel,target,guild,role_ids,cat):
        if target is None:
            return

        roles=[guild.get_role(int(_id_)) for _id_ in str(role_ids).split(",") if len(_id_)]
        await target.edit(roles=roles)
        self.db.removeMute(guild.id,target.id,cat)

        if channel is not None:
            em=discord.Embed(
                    title="**`Member Unmuted`**",
                    description=f"`{target.display_name} was unmuted in {guild.name} thanks to Time Duration Ending`",
                    color=discord.Color.from_rgb(41,41,41),
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    timestamp=dt.utcnow()
                )
            em.set_thumbnail(url=target.avatar.url)
            fields=[
                ("**__`Member`__**","`{}`".format(target.display_name),False),
                ("**__`Reason`__**","`Muted due to Time Deprecation, Unmuted because Time-Duration had ended`",False)
            ]
            for name, value, inline in fields:
                em.add_field(name=name, value=value, inline=inline)
            await channel.send(embed=em)
            await target.send(embed=em)
            
                

    async def unmute(self,ctx,targets,*,reason="`No Reason was Provided`"):
        for target in targets:
            if target is None:
                continue

            if ctx.guild.get_role(self.db.getMutedRole(ctx.guild.id)) in target.roles:
                role_ids=self.db.getRoleID(ctx.guild.id,target.id,'undefined-mutes')
                roles=[ctx.guild.get_role(int(_id_)) for _id_ in role_ids.split(",") if len(_id_)]
                self.db.removeMute(ctx.guild.id,target.id,'undefined-mutes')

                await target.edit(roles=roles)

                em=discord.Embed(
                    title="**`Member Unmuted`**",
                    description=f"`{target.display_name} was unmuted in {ctx.guild.name} thanks to {ctx.author.display_name}`",
                    color=discord.Color.from_rgb(41,41,41),
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    timestamp=dt.utcnow()
                )
                em.set_thumbnail(url=target.avatar.url)
                em.set_author(name=ctx.author.display_name,url=ctx.author.avatar.url,icon_url=ctx.author.avatar.url)

                fields=[
                    ("**__`Member`**__","`{}`".format(target.display_name),False),
                    ("**__`Reason`**__","`{}`".format(reason),False)
                ]
                for name, value, inline in fields:
                    em.add_field(name=name, value=value, inline=inline)

                await ctx.channel.send(embed=em)
                if self.db.getLogChannel(ctx.guild.id) is None:
                        await ctx.channel.send("**`Warning, Log Channel is not Specified, this will NOT be logged, kindly specify a Log Channel`**")
                else:
                    await ctx.guild.get_channel(self.db.getLogChannel(ctx.guild.id)).send(embed=em)
                await target.send(embed=em)



    @commands.command(name="mute",aliases=['shut','shutup','adultsaretalking','freeze'])
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True,manage_guild=True)
    async def mute_command(self,ctx,members:Greedy[Member],given_time:Optional[str],*,reason: Optional[str]='`No Reason was Provided`'):
        if given_time:
            sliced=[]
            sliced[:]=given_time
            hours=int("".join(sliced[:-1]))
            unit=sliced[-1:][0]
            #Errors
            given_time=hours

            if not(unit in ['m','h','d']):
                return await ctx.channel.send("`You sent an Unidentified Unit, There are currently 3 units - Hours/h , Minutes/m , Seconds/s`")

            if unit=='m' and (given_time<5 or given_time>59):
                return await ctx.channel.send(f"`You can use a Minute mute ranging from 5m to 59m, not {given_time}m`")
            elif unit=='h' and (given_time<1 or given_time>59):
                return await ctx.channel.send(f"`You can use an Hour mute ranging from 1h to 59h, not {given_time}h")
            elif unit=='d' and (given_time<1 or given_time>30):
                return await ctx.channel.send(f"`You can use a Day mute ranging from 1d to 30d, not {given_time}d")

            if unit=='m':
                given_time=hours*60
            elif unit=='h':
                given_time=hours*3600
            elif unit=='d':
                given_time=hours*216000

        else:
            given_time=0
            unit=None
        
                
        if not(len(members)):
            return await ctx.channel.send("`You did not specify any Member(s) to mute!`")
        unmutes=[]

        if self.db.checkForGuild(ctx.guild.id):
            await ctx.channel.send("`You were not logged in the Database, Logging in...`")
        if self.db.getMutedRole(ctx.guild.id) is None:
            return await ctx.channel.send("`You haven't assigned a Mute Role, Kindly assign one`")
        mute_role=ctx.guild.get_role(self.db.getMutedRole(ctx.guild.id))

        for t in members:
            if not mute_role in t.roles:
                if ctx.guild.me.top_role.position>t.top_role.position:
                    role_ids=",".join([str(r.id) for r in t.roles])
                    end_time=dt.utcnow()+datetime.timedelta(seconds=given_time) if given_time != 0 else None

                    if unit is not None:
                        if unit=='m':
                            cat='minute-mutes'
                        elif unit=='h':
                            cat='hour-mutes'
                        else:
                            cat='day-mutes'
                    else:
                        cat='undefined-mutes'
                    self.db.addMute(ctx.guild.id,t.id,role_ids,end_time if end_time is not None else None,cat)
                    await t.edit(roles=[mute_role])

                    em=discord.Embed(
                        title="**`Member Mute(s)`**",
                        description=f"`{t.display_name} was Muted in {ctx.guild.name} by {ctx.author.display_name}`",
                        color=discord.Color.from_rgb(41,41,41),
                        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        timestamp=dt.utcnow()
                    )

                    em.set_author(name=ctx.author,icon_url=ctx.author.avatar.url,url=ctx.author.avatar.url)
                    em.set_thumbnail(url=t.avatar.url)

                    fields=[
                        ("__`Member`__", t.display_name, False),
                        ("__`Muted by`__", ctx.author.display_name, False),
                        ("__`Duration`__", f"`{hours}{unit}(s)`" if given_time!=0 else "`Unspecified/Indefinite`", False),
                        ("__`Reason`__", reason, False)
                    ]
                    for name, value, inline in fields:
                        em.add_field(name=name, value=value, inline=inline)

                    await ctx.channel.send(embed=em)
                    await t.send(embed=em)
                    if self.db.getLogChannel(ctx.guild.id) is None:
                        await ctx.channel.send("**`Warning, Log Channel is not Specified, this will NOT be logged, kindly specify a Log Channel`**")
                    else:
                        await ctx.guild.get_channel(self.db.getLogChannel(ctx.guild.id)).send(embed=em)

                    if given_time:
                        unmutes.append(t)
                else:
                    await ctx.channel.send(f"`{t.display_name} could not be Muted`")
            else:
                await ctx.channel.send(f"`{t.display_name} is Already Muted!`")
    
    @mute_command.error
    async def mute_command_error(self,ctx,error):
        print(error)
        if isinstance(error,MissingRequiredArgument):
            return await ctx.channel.send(f"`Missing a Required Arguement || Format is - {self.bot.prefix}mute @member`")
        
        elif isinstance(error, CheckFailure):
            return await ctx.channel.send(f"`You are missing a required permission`")

        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {self.bot._encrypt(str(error))}`")    
    
    async def on_command_error(self,ctx,error):
        if isinstance(error, CommandNotFound):
            return await ctx.channel.send("**`Couldn't find the specified command`**")

        elif isinstance(error, Forbidden):
            return await ctx.channel.send("**`I do not have the permission to do the specified task`**")
        
        elif isinstance(error, HTTPException):
            return await ctx.channel.send("**`Unable to Request from Discord, Please try again later`**")
        
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")    
        
    @commands.command(name='unmute',aliases=['unshut','adultsarenttalking','thaw'])
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True,manage_guild=True)
    async def unmute_command(self,ctx, targets:Greedy[Member], *, reason:Optional[str]="`No Reason was Provided`"):
        if not len(targets):
            return await ctx.channel.send(f"`You did not Speficy any Targets! One or More Required`")
        await self.unmute(ctx,targets,reason=reason)
    
    @unmute_command.error
    async def unmute_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.channel.send("`You did not specify the Member(s) to Unmute!`")
        elif isinstance(error,Forbidden):
            await ctx.channel.send("`I am missing a Permission`")
        
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")     


    '''TASKS'''
    async def unmuter_task(self,member,guild,roleID,timestamp,channel,cat):
        await sleep_until(timestamp)
        await self.cunm(channel=channel,target=member,guild=guild,role_ids=roleID,cat=cat)

    @tasks.loop(minutes=5)
    async def minute_mute_checker(self):
        for guild in self.bot.guilds:
            x=self.db.getMutes(guild.id,cat='minute-mutes')
            for i in list(x.keys()):
                timem=x[i]['end_time']
                if timem>dt.utcnow()+datetime.timedelta(minutes=5):
                    continue 
                else:
                    roleIDS=x[i]['roles']
                    member=await guild.fetch_member(int(i))
                    channel=guild.get_channel(self.db.getLogChannel(guild.id))
                    await self.bot.loop.create_task(self.unmuter_task(member,guild,roleIDS,timem,channel,cat='minute-mutes'))
    
    @tasks.loop(hours=1)
    async def hour_mute_checker(self):
        for guild in self.bot.guilds:
            x=self.db.getMutes(guild.id,cat='hour-mutes')
            for i in list(x.keys()):
                timem=x[i]['end_time']
                if timem>dt.utcnow()+datetime.timedelta(hours=1):
                    continue 
                else:
                    roleIDS=x[i]['roles']
                    member=await guild.fetch_member(int(i))
                    channel=guild.get_channel(self.db.getLogChannel(guild.id))
                    await self.bot.loop.create_task(self.unmuter_task(member,guild,roleIDS,timem,channel,cat='hour-mutes'))
    
    @tasks.loop(hours=24)
    async def day_mute_checker(self):
        for guild in self.bot.guilds:
            x=self.db.getMutes(guild.id,cat='day-mutes')
            for i in list(x.keys()):
                timem=x[i]['end_time']
                if timem>dt.utcnow()+datetime.timedelta(hours=24):
                    continue 
                else:
                    roleIDS=x[i]['roles']
                    member=await guild.fetch_member(int(i))
                    channel=guild.get_channel(self.db.getLogChannel(guild.id))
                    await self.bot.loop.create_task(self.unmuter_task(member,guild,roleIDS,timem,channel,cat='day-mutes')) 

    @minute_mute_checker.before_loop
    async def printer_min(self):
        await self.bot.wait_until_ready()
        await sleep(5)
    
    @minute_mute_checker.before_loop
    async def printer_hr(self):
        await self.bot.wait_until_ready()
        await sleep(5)
    
    @minute_mute_checker.before_loop
    async def printer_day(self):
        await self.bot.wait_until_ready()
        await sleep(5)

    @tasks.loop(minutes=30)
    async def save_file(self):
        await self.bot.wait_until_ready()
        self.db.save()
        await sleep(5)
        print(f"Successfully saved || UTC - {dt.utcnow()}")
        print('_________________________________________________')

def setup(bot):
    bot.add_cog(Mute(bot))