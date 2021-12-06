import nextcord as discord
from nextcord.ext.commands import command, group, Cog
from typing import Optional
from functools import lru_cache
from sys import setrecursionlimit
setrecursionlimit(10**7)

import math

class MathFun(Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @lru_cache(maxsize=5)
    def fib(self,n):
        if n<=1:return n
        return self.fib(n-1)+self.fib(n-2)

    @group(name="math",aliases=['calc'],invoke_without_command=True)
    async def math_command(self,ctx,func:Optional[str]='',num:Optional[int]=0):
        func=func.lower()
        try:
            if num>100:
                return await ctx.send("`Cannot Calculate Advanced Math Functions over 100`")
            if func in ['e','inf','nan','pi','tau']:
                thing='{}'
                num=""
            else:
                thing='({})'
            await ctx.send("`Math Result : {}`".format(round(eval("".join(['math.',func,thing.format(num)])),3)))
        except Exception:
            await ctx.send("`Math Commands!`")

    @math_command.command(name="solve",aliases=['do','calc'])
    async def solve_command(self,ctx,*,exp:Optional[str]='1+1'):
        if len(exp)>50:
            return await ctx.send("`Cannot calculate More than 50 Characters of Literals.`")

        await ctx.send(f"`The Answer to this expression is {eval(exp)}`")

    @math_command.command(name="add",aliases=['plus','sum'])
    async def add_command(self,ctx,num1:Optional[int]=69,num2:Optional[int]=420):
        if (num1>1000000000000) or (num2>1000000000000):
            return await ctx.send("`I cannot calculate addition above 1,000,000,000,000`")
        await ctx.send(f"`{num1} + {num2} = {num1+num2}`")

    @math_command.command(name="sub",aliases=['remov'])
    async def sub_command(self,ctx,num1:Optional[int]=69,num2:Optional[int]=420):
        if (num1>1000000000000) or (num2>1000000000000):
            return await ctx.send("`I cannot calculate subtraction above 1,000,000,000,000`")
        await ctx.send(f"`{num1} - {num2} = {num1-num2}`")

    @math_command.command(name="mult",aliases=['into'])
    async def mult_command(self,ctx,num1:Optional[int]=69,num2:Optional[int]=420):
        if (num1>100000) or (num2>100000):
            return await ctx.send("`I cannot calculate multiplication above 100,000`")
        await ctx.send(f"`{num1} x {num2} = {num1*num2}`")

    @math_command.command(name="div")
    async def div_command(self,ctx,num1:Optional[int]=69,num2:Optional[int]=420):
        if (num1>10000) or (num2>10000):
            return await ctx.send("`I cannot calculate division above 10,000`")
        if (num1==0) or (num2==0):
            return await ctx.send("`Cannot divide by/or Zero`")
        await ctx.send(f"`{num1} / {num2} = {round(num1/num2,4)}`")

    @math_command.command(name="fibnum")
    async def fibnum_command(self,ctx,n:Optional[int]=0):
        if n>1420:
            return await ctx.send("`I cannot calculate Fibonacci over 1420 times!`")

        return await ctx.send(f"`The {n}th number in the Fibonacci Sequence is {self.fib(n)}`")

    @math_command.command(name="exp",aliases=['raise'])
    async def exp_command(self,ctx,n:Optional[int]=1,n2:Optional[int]=1):
        if (n>69) or (n2>100):
            return await ctx.send("`I cannot Exponentialize The First number which is more than 69 or Use the Power of {}`".format(n2))
        await ctx.send(f"`{n} ^ {n2} = {n**n2}`")

    @math_command.command(name="sqrt",aliases=['root'])
    async def sqrt_command(self,ctx,n:Optional[int]=1):
        if (n>420) :
            return await ctx.send("`I cannot Sq.Root the number which is more than 420`".format(n))
        await ctx.send(f"`root {n} = {round(math.sqrt(n),4)}`")


def setup(bot):
    bot.add_cog(MathFun(bot))