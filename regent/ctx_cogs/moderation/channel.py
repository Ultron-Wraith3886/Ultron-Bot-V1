import random
import nextcord as discord
from asyncio import sleep
from typing import Optional
from nextcord.ext import commands
from nextcord.ext.commands import Cog

from nextcord import Forbidden, TextChannel, HTTPException
from nextcord.ext.commands import Greedy, bot_has_permissions, has_permissions, MissingRequiredArgument, BadArgument, CommandNotFound, CheckFailure

class ChannelModeration(Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(name='lockchannel',aliases=['lock','block','prisonchat','lockdown'])
    @has_permissions(manage_channels=True)
    @bot_has_permissions(manage_channels=True)
    async def lockchannel_command(self,ctx,channels:Greedy[TextChannel]=None):
        if not channels:
            channels=[ctx.channel]

        for channel in channels:
            if ctx.guild.default_role not in channel.overwrites:
                ow={ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)}
                await channel.send(f"**__`Channel was Locked Down by {ctx.author.display_name}`__**")
                await channel.edit(overwrites=ow)
            elif channel.overwrites[ctx.guild.default_role].send_messages==True or channel.overwrites[ctx.guild.default_role].send_messages==None:
                ow=channel.overwrites[ctx.guild.default_role]
                ow.send_messages=False
                await channel.send(f"**__`Channel was Locked Down by {ctx.author.display_name}`__**")
                point=random.randint(1,1024)
                if point==1:
                    await ctx.channel.send("https://tenor.com/view/za-warudo-toki-wo-tomare-gif-8629953")
                await channel.set_permissions(ctx.guild.default_role,overwrite=ow)
            else:
                await ctx.channel.send(f"**__`This channel is already Locked Down, Perhaps use {self.bot.prefix}unlock`__**")
    
    @lockchannel_command.error
    async def lockchannel_command_error(self,ctx,error):
        if isinstance(error,MissingRequiredArgument):
            await ctx.channel.send("`You are Missing a Required Argument`")
        elif isinstance(error, Forbidden):
            await ctx.channel.send("`I am missing a Permission!`")
        elif isinstance(error, CheckFailure):
            await ctx.channel.send("`You are missing a Permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")  
        
    @commands.command(name='unlockchannel',aliases=['unlock','unblock','unprisonchat','unlockdown'])
    @has_permissions(manage_channels=True)
    @bot_has_permissions(manage_channels=True)
    async def unlockchannel_command(self,ctx,channels:Greedy[TextChannel]):
        if not channels:
            channels=[ctx.channel]
        for channel in channels:
            if channel.overwrites[ctx.guild.default_role].send_messages==False:
                ow=channel.overwrites[ctx.guild.default_role]
                ow.send_messages=None
                await channel.set_permissions(ctx.guild.default_role,overwrite=ow)
                point=random.randint(1,1024)
                if point==1:
                    await ctx.channel.send("https://tenor.com/view/thanos-time-rewindtime-timestone-gif-19399835")
                await ctx.channel.send(f"**__`This Channel was Unlocked by {ctx.author.display_name}`__**")

            else:
                await ctx.author.send(f"**__`This channel {channel.name} is already Unlocked, Perhaps use {self.bot.prefix}lock to Lock channels`__**")

    @unlockchannel_command.error
    async def unlockchannel_command_error(self,ctx,error):
        if isinstance(error,MissingRequiredArgument):
            await ctx.channel.send("`You are Missing a Required Argument`")
        elif isinstance(error, Forbidden):
            await ctx.channel.send("`I am missing a permission!`")
        elif isinstance(error, CheckFailure):
            await ctx.channel.send("`You are missing a permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")     
        
    @commands.command(name="purge",aliases=['massdelete','deleterange'])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def purge_command(self,ctx,messages:Optional[int],channels:Greedy[TextChannel]):
        if not channels:
            channels=[ctx.channel]
        if len(channels)>3:
            return await ctx.channel.send("`The Channel amount is greater than 3, I can only purge a Max of 3 Channels`")
        
        if not messages:
            messages=10

        if messages>169:
            return await ctx.channel.send("`I cannot purge more than 169 Messages`")
            await ctx.channel.send("`You didn't specify the Purge Amount, Setting to 10 Messages`")
        

        for channel in channels:
            deleted=await channel.purge(limit=messages)
            sent=await channel.send(f"`Deleted {len(deleted)} messages from {channel.name} as requested by {ctx.author.display_name} || This message will be deleted after 5 Seconds`")
            await sent.delete(delay=5.00)

    @purge_command.error
    async def purge_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.channel.send("`You are missing a Required Argument`")
        elif isinstance(error, Forbidden):
            await ctx.channel.send("`I am missing a Permission!`")
        elif isinstance(error, CheckFailure):
            await ctx.channel.send("`You are missing a Permission`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`") 
    
    @commands.command(name="slowmode",aliases=['slowchat','calmdownman','slow'])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def slowmode_command(self,ctx,delay:Optional[str]='5s',channels:Greedy[TextChannel]=None):
        if not channels:
            channels=[ctx.channel]
        
        sliced=[]
        sliced[:]=delay
        try:
            delay=int("".join(sliced[:-1]))
        except:
            delay=1
        unit=sliced[-1:][0]

        if not unit in ['s','m','h'] or (unit=='h' and unit>6):
            return await ctx.send(f"`You cannot set the Slowmode to More than 6 Hours || Current unit types are - 's' , 'm' , 'h' for seconds, minutes and hours respectively`")
        
        if len(channels)>3:
            return await ctx.send("`You cannot choose more than 3 Channels to Apply Slowmode to, Refrain from using 3 Channels`")

        for channel in channels:
            await channel.send(f"`This channel {ctx.channel.name} has been changed to apply slowmode with a delay of {delay}{unit} by {ctx.author.display_name}`")
            await channel.edit(slowmode_delay=delay)
    
    @commands.command(name="unslowmode",aliases=['unslowchat','unslow'])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def unslowmode_command(self,ctx,channels:Greedy[TextChannel]=None):
        if not channels:
            channels=[ctx.channel]

        for channel in channels:
            await channel.send(f"`This channel {ctx.channel.name} was unslow-moded by {ctx.author}`")
            await channel.edit(slowmode_delay=0)

    @unslowmode_command.error
    async def unslowmode_command_error(self,ctx,error):
        if isinstance(error,Forbidden):
            await ctx.send("`I do not have a required permission to unslowmode`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission to unslowmode`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`") 

    @slowmode_command.error
    async def slowmode_command_error(self,ctx,error):
        if isinstance(error, Forbidden):
            await ctx.send("`I do not have permission to change Slowmode!`")
        
        elif isinstance(error, CheckFailure):
            await ctx.send("`You do not have the permission to change Slowmode!`")
        
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`") 
    
    async def on_command_error(self,ctx,error):
        if isinstance(error, CommandNotFound):
            return await ctx.send("**`Couldn't find the specified command`**")

        elif isinstance(error, Forbidden):
            return await ctx.send("**`I do not have the permission to do the specified task`**")
        
        elif isinstance(error, HTTPException):
            return await ctx.send("**`Unable to Request from Discord, Please try again later`**")
        
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")  
    
    @commands.command(name='addlog',aliases=['setlog'])
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def addlog_command(self,ctx,log:TextChannel):
        self.bot.db.addLogChannel(ctx.guild.id, log.id)
            
        await ctx.send(f"`Registered {log.name} as Log Channel`")
def setup(bot):
    bot.add_cog(ChannelModeration(bot))