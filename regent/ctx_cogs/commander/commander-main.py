import nextcord as discord
from nextcord.ext.commands import is_owner, Cog, group,command
from typing import Optional

import psutil
from platform import processor as prc

class Evaluator(Cog):
    def __init__(self,bot):
        self.bot=bot

    @group(name="eval",invoke_without_command=True)
    @is_owner()
    async def eval_grp(self,ctx,*,command:Optional[str]=''):
        try:
            await ctx.send(eval(command))
        except Exception as e:
            await ctx.send(e)

    @eval_grp.command(name='msg')
    @is_owner()
    async def msg_eval(self,ctx,msgid:int):
        msg=await ctx.channel.fetch_message(msgid)
        try:
            await ctx.send(eval(msg.content))
        except Exception as e:
            await ctx.send(e)

    @is_owner()
    @command(name='ping',aliases=['latency'])
    async def latency_command(self,ctx):
        await ctx.send("{}{}".format(round(self.bot.latency*1000),'ms'))

    @is_owner()
    @command(name='system',aliases=['sysinfo'])
    async def sysinfo_command(self,ctx):
        cpu_cnt=psutil.cpu_count(logical=False)
        proc=prc()
        vmem=psutil.virtual_memory()
        mem=vmem.percent
        mem_tot=vmem.total
        mem_ava=vmem.available*100/mem_tot
        mem_use=mem_tot-mem_ava
        em=discord.Embed(
            title='**`System Information`**',
            color=discord.Color.from_rgb(0,0,0)
        )
        fields=[
            ('**`CPU Count`**',cpu_cnt,False),
            ('**`Processor`**',proc if proc else 'Not Specified',False),
            ('**`Memory Usage`**',f"`{round((mem_use/1e+6)*100)/100}mb/{round((mem_tot/1e+6)*100)/100}mb || {round((mem_ava)*100)/100}mb Available || {mem}% Used`",False)
        ]
        for name,value,inline in fields:
            em.add_field(name=name,value=value,inline=inline)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Evaluator(bot))
    
