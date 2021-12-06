from nextcord.ext.commands import command,Cog
from sympy import Symbol
from sympy.solvers import solve

class LinearEQ(Cog):
    def __init__(self,bot):
        self.bot=bot

    def iscof(self,inp):
        return any(c.isdigit() for c in inp)

    def isfloat(self,num):
        try:
            float(num)
            return True 
        except:
            return False

    async def qsolve(self,inp):
        inp = inp.split(sep='=',maxsplit=1)
        lhs=inp[0].split()
        newlhs=[]
        newrhs=[]
        
        for indx,term in enumerate(lhs):
            if self.iscof(term):
                num="".join([str(int(s)) if s.isdigit() else s for s in term])
                if self.isfloat(num):
                    num=str(float(num))
                arith_op='*'
                var="".join([s if s.isalpha() else '' for s in term])
                if var == '':
                    var='1'
                newlhs.extend([num,arith_op,var])
            else:
                newlhs.append(term)

        #rhs=int(round(eval("".join(inp[1].split()))))

        rhs=inp[1].split()
        for indx,term in enumerate(rhs):
            if self.iscof(term):
                num="".join([str(int(s)) if s.isdigit() else s for s in term])
                if self.isfloat(num):
                    num=str(float(num))
                arith_op='*'
                var="".join([s if s.isalpha() else '' for s in term])
                if var == '':
                    var='1'
                newrhs.extend([num,arith_op,var])
            else:
                newrhs.append(term)
                
        arith_ops=['+','-','*','/']
        lt_ce=0
        for indx,itm in enumerate(newlhs):
            if not itm in arith_ops:
                if itm.isalpha():
                    lt_ce=Symbol(itm)
                    newlhs=''.join(newlhs).replace(itm,'lt_ce')

        for indx,itm in enumerate(newrhs):
            if not itm in arith_ops:
                if itm.isalpha():
                    lt_ce=Symbol(itm)
                    newrhs=''.join(newrhs).replace(itm,'lt_ce')
        

        solved=solve(eval(''.join(newlhs))-eval(''.join(newrhs)),lt_ce)
        
        return lt_ce,solved[0]

    @command(name='lineareq',aliases=['leq'])
    async def linear_eq(self,ctx,*,eq):
        await self.qsolve(eq)
        try:
            v,s=await self.qsolve(eq)
            await ctx.send(f"`{v}` in this Linear Equation is `{round(float(s),3)}`")
        except Exception as e:
            print(e)
            await ctx.send("`Couldn't solve`")

def setup(bot):
    bot.add_cog(LinearEQ(bot))