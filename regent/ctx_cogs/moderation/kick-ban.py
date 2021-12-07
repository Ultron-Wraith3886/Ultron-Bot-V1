import nextcord as discord
from nextcord.ext import commands

from typing import Optional
from datetime import datetime as dt

#Classes
from nextcord import Member

from nextcord.ext.commands import Cog, Greedy

from nextcord import HTTPException, Forbidden
from nextcord.ext.commands import Cog, Greedy
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands import MissingRequiredArgument, BadArgument, has_permissions, bot_has_permissions, CheckFailure

class KickBanModeration(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.db=self.bot.db
    
    @commands.command(name='kick',aliases=['remove','fuckoff','farewell'])
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    async def kick_command(self,ctx,targets:Greedy[Member],*,reason:Optional[str]="`No reason was Provided`"):
        if not len(targets):
            return await ctx.channel.send("`You didn't specify any Members. Kindly do so if you want to Kick some`")
        
        for target in targets:
            if ctx.guild.me.top_role.position>target.top_role.position and not target.guild_permissions.administrator:
                
                em=discord.Embed(
                    title="**`Member was Kicked`**",
                    description=f"`{target.display_name} was kicked from {ctx.guild.name} by {ctx.author.display_name}",
                    color=discord.Color.from_rgb(41,41,41),
                    url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    timestamp=dt.now()
                )
                em.set_author(name=ctx.author.display_name,url=ctx.author.avatar.url,icon_url=ctx.author.avatar.url)
                em.set_thumbnail(name=target.avatar.url)
                fields=[
                    ('**__`Member`__**',"`{}`".format(target.display_name),False),
                    ('**__`Kicked By`__**',"`{}`".format(ctx.author.display_name),False),
                    ('**__`Reason`__**',"`{}`".format(reason),False)
                ]
                for name,value,inline in fields:
                    em.add_field(name=name,value=value,inline=inline)

                channel=self.db.getLogChannel(ctx.guild.id)
                if channel is None:
                    await ctx.channel.send("**`Warning, Log Channel is not Specified, this will NOT be logged, kindly specify a Log Channel`**")
                else:
                    await ctx.guild.get_channel(channel).send(embed=em)
                await ctx.channel.send(embed=em)
                await target.send(embed=em)
                await target.kick(reason=reason)
            else:
                await ctx.channel.send(f"`{target.display_name} couldn't be banned`")
        
    
    @kick_command.error
    async def kick_command_error(self,ctx,error):
        if isinstance(error,CheckFailure):
            await ctx.channel.send(f"`Insufficient Permissions to Execute the given Command|| Pro Tip - Maybe you missed some permissions!  || Error: {error}`")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.channel.send(f"`Insufficient Parameters to Execute the given Command || Pro Tip - Maybe you missed some parameters! || Error: {error} || Format is - {self.bot.prefix}kick @member`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")     
    
    @commands.command(name='ban',aliases=['begonethot','banmember','permkick','broyourereallyannoyingnowbegone'])
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def ban_command(self,ctx,targets:Greedy[Member],*,reason:Optional[str]="`No reason was Provided`"):
        if not len(targets):
            return await ctx.channel.send("`You didn't specify any Members. Kindly do so if you want to ban some`")
        
        for target in targets:
            em=discord.Embed(
                title="**`Member was Banned`**",
                description=f"`{target.display_name} was banned from {ctx.guild.name} by {ctx.author.display_name}",
                color=discord.Color.from_rgb(41,41,41),
                url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                timestamp=dt.now()
            )
            em.set_author(name=ctx.author.display_name,url=ctx.author.avatar.url,icon_url=ctx.author.avatar.url)
            em.set_thumbnail(name=target.avatar.url)
            fields=[
                ('**__`Member`__**',"`{}`".format(target.display_name),False),
                ('**__`Banned By`__**',"`{}`".format(ctx.author.display_name),False),
                ('**__`Reason`__**',"`{}`".format(reason),False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)

            channel=self.db.getLogChannel(ctx.guild.id)
            if channel is None:
                await ctx.channel.send("**`Warning, Log Channel is not Specified, this will NOT be logged, kindly specify a Log Channel`**")
            else:
                await ctx.guild.get_channel(channel).send(embed=em)
            await ctx.channel.send(embed=em)
            await target.send(embed=em)
            await target.ban(reason=reason)
    
    @ban_command.error
    async def ban_command_error(self,ctx,error):
        if isinstance(error,CheckFailure):
            await ctx.channel.send(f"`Insufficient Permissions to Execute the given Command|| Pro Tip - Maybe you missed some permissions!  || Error: {error}`")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.channel.send(f"`Insufficient Parameters to Execute the given Command || Pro Tip - Maybe you missed some parameters! || Error: {error} || Format is - {self.bot.prefix}ban @member`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")   
        
    @commands.command(name='unban',aliases=['comeback','jailbreak','returnofthelegend'])
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def unban_command(self,ctx,targets:Greedy[int],*,reason:Optional[str]="`No reason was Provided`"):
        if not len(targets):
            return await ctx.channel.send("`You didn't specify any Members. Kindly do so if you want to unban some`")
        
        for t in targets:
            target=await self.bot.fetch_user(t)
            await target.unban(reason=reason)
            em=discord.Embed(
                title="**`Member was Unbanned`**",
                description=f"`{target.display_name} was Unbanned from {ctx.guild.name} by {ctx.author.display_name}",
                color=discord.Color.from_rgb(41,41,41),
                url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                timestamp=dt.now()
            )
            em.set_author(name=ctx.author.display_name,url=ctx.author.avatar.url,icon_url=ctx.author.avatar.url)
            em.set_thumbnail(name=target.avatar.url)
            fields=[
                ('**__`Member`__**',"`{}`".format(target.display_name),False),
                ('**__`Unbanned By`__**',"`{}`".format(ctx.author.display_name),False),
                ('**__`Reason`__**',"`{}`".format(reason),False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)

            channel=self.db.getLogChannel(ctx.guild.id)
            if channel is None:
                await ctx.channel.send("**`Warning, Log Channel is not Specified, this will NOT be logged, kindly specify a Log Channel`**")
            else:
                await ctx.guild.get_channel(channel).send(embed=em)
            await ctx.channel.send(embed=em)
            await target.send(embed=em)
    
    @unban_command.error
    async def unban_command_error(self,ctx,error):
        if isinstance(error,CheckFailure):
            await ctx.channel.send(f"`Insufficient Permissions to Execute the given Command|| Pro Tip - Maybe you missed some permissions!  || Error: {error}`")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.channel.send(f"`Insufficient Parameters to Execute the given Command || Pro Tip - Maybe you missed some parameters! || Error: {error} || Format is - {self.bot.prefix}unban @member`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")    


def setup(bot):
    bot.add_cog(KickBanModeration(bot))