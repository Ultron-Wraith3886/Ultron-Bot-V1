import nextcord as discord
from nextcord.ext import commands
from typing import Optional
from datetime import datetime as dt

from nextcord import Role, Member, VoiceChannel

from nextcord.ext.commands import Greedy, Cog
from nextcord import Forbidden
from nextcord.ext.commands import MissingRequiredArgument, BadArgument, has_permissions, bot_has_permissions, CheckFailure

class MemberModeration(Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command(name="multiaddrole",aliases=['multimemberrole'])
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def multiple_addrolemember_command(self,ctx,*,role:Role,members:Greedy[Member]=None,reason:Optional[str]='No Reason was Provided'):
        if members is None:
            members=[ctx.author]
        elif len(members)>6:
            await ctx.send("`You can only add roles to 6 Members at a time!`")
        for member in members:
            if ctx.guild.me.top_role.position>member.top_role.position:
                await member.add_roles(role,reason=reason)
                em=discord.Embed(
                    title='**`Added role to Member`**',
                    description=f'**`{ctx.author.display_name}`**`added {role.name} to `**`{member.display_name}`**',
                    color=discord.Color.from_rgb(0,0,0),
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    timestamp=dt.now()
                )
                fields=[
                    ("__Member__",member.display_name,False),
                    ("__Role__",role.mention,False),
                    ("__Added By__",ctx.author.display_name,False),
                    ("__Reason__",reason,False)
                ]
                for name,value,inline in fields:
                    em.add_field(name=name,value=value,inline=inline)
                em.set_thumbnail(url=member.avatar.url)
                await ctx.send(embed=em)
                await member.send(embed=em)
                logchan=self.bot.db.getLogChannel(ctx.guild.id)
                if logchan is not None:
                    await self.guild.get_channel().send(embed=em)
                else:
                    await ctx.channel.send("`This server doesn't have an assigned log channel, Kindly do it`")
            else:
                await ctx.send(f"`Couldn't add roles to {member.display_name} because their Top Role is higher than mine!`")

    @multiple_addrolemember_command.error
    async def multiple_addrolemember_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")
        


    @commands.command(name="multiappendrole",aliases=['multirole'])
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def multiple_appendrole_command(self,ctx,member:Member,roles:Greedy[Role],reason:Optional[str]='No Reason was Provided'):

        if len(roles)>10:
            return await ctx.send("`You can only add 10 Roles at a time!`")
         
        if not ctx.guild.me.top_role.position>member.top_role.position:
            return await ctx.send(f"`I cannot add roles to {member.display_name} as their Top Role is higher than mine!`")
        
        await member.add_roles(*roles,reason=reason)
        
        em=discord.Embed(
            title='**`Added Role(s)`**',
            description=f"**`{ctx.author.display_name}`**` to`**`{member.display_name}`**",
            color=discord.Color.from_rgb(0,0,0),
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            timestamp=dt.now()
        )
        fields=[
            ("__Role(s)__",[role.name for role in roles],False),
            ("__Added to__",member.display_name,False),
            ("__Added By__",ctx.author.display_name,False),
            ("__Reason__",reason,False)
        ]
        for name,value,inline in fields:
            em.add_field(name=name,value=value,inline=inline)
        em.set_thumbnail(url=member.avatar.url)
        
        await ctx.send(embed=em)
        await member.send(embed=em)

        logchan=self.bot.db.getLogChannel(ctx.guild.id)
        if logchan is not None:
            await ctx.guild.get_channel(logchan).send(embed=em)
        else:
            await ctx.send("`You haven't assigned a Log Channel, Kindly do it`")

    @multiple_appendrole_command.error
    async def multiple_appendrole_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")


    @commands.command(name="role",aliases=['singlerole'])
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def appendrole_command(self,ctx,member:Member,role:Role,reason:Optional[str]='No Reason was Provided'):
        if not ctx.guild.me.top_role.position>member.top_role.position:
            return await ctx.send(f"`I cannot add roles to {member.display_name} as their Top Role is higher than mine!`")

        await member.add_roles(role,reason=reason)
        em=discord.Embed(
            title='**`Added Role(s)`**',
            description=f"**`{ctx.author.display_name}`**` Added roles to `**`{member.display_name}`**",
            color=discord.Color.from_rgb(0,0,0),
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            timestamp=dt.now()
        )
        fields=[
            ("__Role(s)__",role.name,False),
            ("__Added to__",member.display_name,False),
            ("__Added By__",ctx.author.display_name,False),
            ("__Reason__",reason,False)
        ]
        for name,value,inline in fields:
            em.add_field(name=name,value=value,inline=inline)
        em.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=em)
        await member.send(embed=em)
        logchan=self.bot.db.getLogChannel(ctx.guild.id)
        if logchan is not None:
            await ctx.guild.get_channel(logchan).send(embed=em)
        else:
            await ctx.send("`You haven't assigned a Log Channel, Kindly do it`")

    @appendrole_command.error
    async def appendrole_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")

    @commands.command(name="removeroles",aliases=['takeroles','unrole'])
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def removeroles_command(self,ctx,member:Member,roles:Greedy[Role],reason:Optional[str]='`No reason was Provided`'):

        if len(roles)>10:
            return await ctx.send("`I cannot remove 10 roles at a time!`")

        if not ctx.guild.me.top_role.position>member.top_role.position:
            return await ctx.send(f"`I cannot take roles from {member.display_name} as their Top Role is higher than mine!`")
        
        await member.remove_roles(*roles,reason=reason)
        em=discord.Embed(
            title='**`Added Role(s)`**',
            description="**`{ctx.author.display_name}`**`remove roles from `**`{member.display_name}`**",
            color=discord.Color.from_rgb(0,0,0),
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            timestamp=dt.now()
        )
        fields=[
            ("__Role(s)__",[role.name for role in roles],False),
            ("__Remove from__",member.display_name,False),
            ("__Remove By__",ctx.author.display_name,False),
            ("__Reason__",reason,False)
        ]
        for name,value,inline in fields:
            em.add_field(name=name,value=value,inline=inline)
        em.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=em)
        await member.send(embed=em)
        logchan=self.bot.db.getLogChannel(ctx.guild.id)
        if logchan is not None:
            await ctx.guild.get_channel(logchan).send(embed=em)
        else:
            await ctx.send("`You haven't assigned a Log Channel, Kindly do it`")

    @removeroles_command.error
    async def removeroles_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")

    @commands.command(name="massremoverole",aliases=['massunrole','multiunrole'])
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def massunrole_command(self,ctx,role:Role,members:Greedy[Member],reason:Optional[str]='`No reason was provided`'):
        if len(members)>6:
            return await ctx.send("`I cannot remove roles from members more than 6 at a time!`")
        
        for member in members:
            if ctx.guild.me.top_role.position>member.top_role.position:
                await member.remove_roles(role,reason=reason)
                em=discord.Embed(
                    title='**`Removed role from Member`**',
                    description=f'**`{ctx.author.display_name}`**` removed roles from `**`{member.display_name}`**',
                    color=discord.Color.from_rgb(0,0,0),
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    timestamp=dt.now()
                )
                fields=[
                    ("__Member__",member.display_name,False),
                    ("__Role__",role.mention,False),
                    ("__Removed By__",ctx.author.display_name,False),
                    ("__Reason__",reason,False)
                ]
                for name,value,inline in fields:
                    em.add_field(name=name,value=value,inline=inline)
                em.set_thumbnail(url=member.avatar.url)
                await ctx.send(embed=em)
                await member.send(embed=em)
                logchan=self.bot.db.getLogChannel(ctx.guild.id)
                if logchan is not None:
                    await self.guild.get_channel().send(embed=em)
                else:
                    await ctx.channel.send("`This server doesn't have an assigned log channel, Kindly do it`")
            else:
                await ctx.send(f"`Couldn't remove roles from {member.display_name} because their Top Role is higher than mine!`")

    @massunrole_command.error
    async def massunrole_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")

    @commands.command(name="nick",aliases=['changenick','nickname'])
    @bot_has_permissions(manage_nicknames=True)
    @has_permissions(manage_nicknames=True)
    async def nick_command(self,ctx,nick:str,members:Greedy[Member]=None,reason:Optional[str]='`No reason was provided`'):
        if members is None:
            members=[ctx.author]
        
        if len(members)>15:
            return await ctx.send("`I cannot change nicknames of more than 15 users at a time!`")

        for member in members:
            await member.edit(nick=nick,reason=reason)
            em=discord.Embed(
                title='**`Changed Member Nickname`**',
                description=f'**`{ctx.author.display_name}`**` changed nickname of `**`{member.display_name}`**',
                color=discord.Color.from_rgb(0,0,0),
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                timestamp=dt.now()
            )
            fields=[
                ("__Member__",member.display_name,False),
                ("__Nickname__",nick,False),
                ("__Changed By__",ctx.author.display_name,False),
                ("__Reason__",reason,False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)
            em.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=em)

    @nick_command.error
    async def nick_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")

    @commands.command(name="vcmute",aliases=['vcshut'])
    @bot_has_permissions(mute_members=True)
    @has_permissions(mute_members=True)
    async def vcmute_command(self,ctx,members:Greedy[Member]=None,reason:Optional[str]='`No reason was Provided`'):
        if members is None:
            members=[ctx.author]

        for member in members:
            await member.edit(mute=True,reason=reason)
            em=discord.Embed(
                title='**`VC-Mute`**',
                description=f'**`{ctx.author.display_name}`**` VC-Muted `**`{member.display_name}`**',
                color=discord.Color.from_rgb(0,0,0),
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                timestamp=dt.now()
            )
            fields=[
                ("__Member__",member.display_name,False),
                ("__Muted By__",ctx.author.display_name,False),
                ("__Reason__",reason,False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)
            em.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=em)
            await member.send(embed=em)
            logchan=self.bot.db.getLogChannel(ctx.guild.id)
            if logchan is not None:
                await self.guild.get_channel().send(embed=em)
            else:
                await ctx.channel.send("`This server doesn't have an assigned log channel, Kindly do it`")

    @vcmute_command.error
    async def vcmute_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")
    
    @commands.command(name="vcunmute",aliases=['vcunshut'])
    @bot_has_permissions(mute_members=True)
    @has_permissions(mute_members=True)
    async def vcunmute_command(self,ctx,members:Greedy[Member]=None,reason:Optional[str]='`No reason was Provided`'):
        if members is None:
            members=[ctx.author]

        for member in members:
            await member.edit(mute=False,reason=reason)
            em=discord.Embed(
                title='**`VC-Unmute`**',
                description=f'**`{ctx.author.display_name}`**` VC-Unmuted `**`{member.display_name}`**',
                color=discord.Color.from_rgb(0,0,0),
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                timestamp=dt.now()
            )
            fields=[
                ("__Member__",member.display_name,False),
                ("__Unmuted By__",ctx.author.display_name,False),
                ("__Reason__",reason,False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)
            em.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=em)
            await member.send(embed=em)
            logchan=self.bot.db.getLogChannel(ctx.guild.id)
            if logchan is not None:
                await self.guild.get_channel().send(embed=em)
            else:
                await ctx.channel.send("`This server doesn't have an assigned log channel, Kindly do it`")
    
    @vcunmute_command.error
    async def vcunmute_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")
        
    @commands.command(name="vcdeafen",aliases=['vcdeaf'])
    @bot_has_permissions(deafen_members=True)
    @has_permissions(deafen_members=True)
    async def vcdeafen_command(self,ctx,members:Greedy[Member]=None,reason:Optional[str]='`No reason was Provided`'):
        if members is None:
            members=[ctx.author]

        for member in members:
            await member.edit(deafen=True,reason=reason)
            em=discord.Embed(
                title='**`VC-Deafen`**',
                description=f'**`{ctx.author.display_name}`**` VC-Defeaned `**`{member.display_name}`**',
                color=discord.Color.from_rgb(0,0,0),
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                timestamp=dt.now()
            )
            fields=[
                ("__Member__",member.display_name,False),
                ("__Deafened By__",ctx.author.display_name,False),
                ("__Reason__",reason,False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)
            em.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=em)
            await member.send(embed=em)
            logchan=self.bot.db.getLogChannel(ctx.guild.id)
            if logchan is not None:
                await self.guild.get_channel().send(embed=em)
            else:
                await ctx.channel.send("`This server doesn't have an assigned log channel, Kindly do it`")

    @vcdeafen_command.error
    async def vcdeafen_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")
    
    @commands.command(name="vcundeafen",aliases=['vcundeaf'])
    @bot_has_permissions(mute_members=True)
    @has_permissions(mute_members=True)
    async def vcundeafen_command(self,ctx,members:Greedy[Member]=None,reason:Optional[str]='`No reason was Provided`'):
        if members is None:
            members=[ctx.author]

        for member in members:
            await member.edit(deafen=False,reason=reason)
            em=discord.Embed(
                title='**`VC-Undeafen`**',
                description=f'**`{ctx.author.display_name}`**` VC-Undeafened `**`{member.display_name}`**',
                color=discord.Color.from_rgb(0,0,0),
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                timestamp=dt.now()
            )
            fields=[
                ("__Member__",member.display_name,False),
                ("__Undeafened By__",ctx.author.display_name,False),
                ("__Reason__",reason,False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)
            em.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=em)
            await member.send(embed=em)
            logchan=self.bot.db.getLogChannel(ctx.guild.id)
            if logchan is not None:
                await self.guild.get_channel().send(embed=em)
            else:
                await ctx.channel.send("`This server doesn't have an assigned log channel, Kindly do it`")
    
    @vcundeafen_command.error
    async def vcundeafen_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")

    @commands.command(name='suppress',aliases=['stagemute'])
    @bot_has_permissions(mute_members=True)
    @has_permissions(mute_members=True)
    async def suppress_command(self,ctx,members:Greedy[Member],reason:Optional[str]='`No reason was provided`'):
        if len(members)>10:
            return await ctx.send("`I cannot suppress more than 10 Members at a time!`")
        
        for member in members:
            await member.edit(suppress=True,reason=reason)
            em=discord.Embed(
                title='**`Stage Suppression`**',
                description=f'**`{ctx.author.display_name}`**` Stage Suppressed `**`{member.display_name}`**',
                color=discord.Color.from_rgb(0,0,0),
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                timestamp=dt.now()
            )
            fields=[
                ("__Member__",member.display_name,False),
                ("__Suppressed By__",ctx.author.display_name,False),
                ("__Reason__",reason,False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)
            em.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=em)
            await member.send(embed=em)

    @suppress_command.error
    async def suppress_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")
    
    @commands.command(name="vcshift",aliases=['vcwarp','vctp'])
    @bot_has_permissions(move_members=True)
    @has_permissions(move_members=True)
    async def movevc_command(self,ctx,vc:VoiceChannel,members:Greedy[Member],reason:Optional[str]='`No reason was provided`'):
        if len(members)>6:
            return await ctx.send("`I cannot move more than 6 members at a time!`")

        for member in members:
            await member.edit(voice_channel=vc,reason=reason)
            em=discord.Embed(
                    title='**`VC Movement by Mod`**',
                    description=f'**`{ctx.author.display_name}`**` moved `**`{member.display_name}`**',
                    color=discord.Color.from_rgb(0,0,0),
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    timestamp=dt.now()
                )
            fields=[
                ("__Member__",member.display_name,False),
                ("__VC___",vc.name,False),
                ("__Moved By__",ctx.author.display_name,False),
                ("__Reason__",reason,False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)
            em.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=em)
            await member.send(embed=em)
        
    @movevc_command.error
    async def movevc_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")
    
    @commands.command(name="vckick",aliases=['vcremove','vck'])
    @bot_has_permissions(move_members=True)
    @has_permissions(move_members=True)
    async def kickvc_command(self,ctx,members:Greedy[Member],reason:Optional[str]='`No reason was provided`'):
        if len(members)>6:
            return await ctx.send("`I cannot move more than 6 members at a time!`")

        for member in members:
            await member.edit(voice_channel=None,reason=reason)
            em=discord.Embed(
                    title='**`VC Kick`**',
                    description=f'**`{ctx.author.display_name}`**` VC-kicked `**`{member.display_name}`**',
                    color=discord.Color.from_rgb(0,0,0),
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    timestamp=dt.now()
                )
            fields=[
                ("__Member__",member.display_name,False),
                ("__Kicked By__",ctx.author.display_name,False),
                ("__Reason__",reason,False)
            ]
            for name,value,inline in fields:
                em.add_field(name=name,value=value,inline=inline)
            em.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=em)
            await member.send(embed=em)
        
    @movevc_command.error
    async def kickvc_command_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("`You are missing a required Argument!`")
        elif isinstance(error, Forbidden):
            await ctx.send("`I do not have a required permission!`")
        elif isinstance(error,CheckFailure):
            await ctx.send("`You do not have a required permission!`")
        else:
            await ctx.channel.send(f"`Something went wrong || Report this Error ID and Error Context to Developers in `[We don't have a Server Yet]` || ID: {await self.bot._encrypt(str(error))}`")

    @commands.command(name="userinfo",aliases=['info'])
    async def userinfo_command(self,ctx,member:Optional[Member]):
        if not member:
            member=ctx.author
        names=[member.display_name,member.name,member.id]
        avatars=[member.avatar.url,member.display_avatar.url]
        if member.banner is not None:
            avatars.append(member.banner.url)
        else:
            avatars.append(None)
        roles=[str(role.name) for role in member.roles]
        infos=[member.created_at.strftime("%d %m %Y"),member.joined_at.strftime("%d %m %Y"),member.guild_permissions,member.pending,member.premium_since.strftime("%d %m %Y") if member.premium_since is not None else None,member.top_role,member.bot,member.is_on_mobile(),member.activity]
        flags=[flag for flag in member.public_flags.all()]
        if self.bot.db.ismuted(ctx.guild.id,member.id):
            muted=True
        else:
            muted=False

        em=discord.Embed(
            title="`Member Information`",
            color=member.color,
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            timestamp=dt.now()
        )
        em.set_author(name=names[1],icon_url=avatars[0],url=avatars[1])
        em.set_thumbnail(url=avatars[1])
        if avatars[2] is not None:
            em.set_image(url=avatars[2])
        fields=[
            ("__Roles__","".join(["`",",".join(roles),"`"]),False),
            ("__Original Name__",names[1],True),
            ("__Server Nickname__",names[0],True),
            ("__Creation & Joined at__",f"Created on `{infos[0]}` and Joined this server on `{infos[1]}`",False),
            ("__Used Nitro Boost on__",infos[4] if infos[4] is not None else "Never boosted",False),
            ("__Top Role__","".join(["`",infos[5].name,"`"]),False),
            ("__Is a Bot?__",infos[6],True),
            ("__Is on Mobile?__",infos[7],True),
            ("__Verification Pending?__",infos[3],True),
            ("__Is Muted?__",muted,True),
            #("__Activity__",infos[8],False),
            ("__Public Flags__",'\n'.join([str(flag)[10:] for flag in flags]),False),
        ]
        for name,value,inline in fields:
            em.add_field(name=name,value=value,inline=inline)
        await ctx.send(embed=em)
        


def setup(bot):
    bot.add_cog(MemberModeration(bot))