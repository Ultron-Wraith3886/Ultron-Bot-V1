from nextcord.ext.commands import Cog,group
from nextcord import Embed,Color
from typing import Optional
import hashlib

class DEVTOOLS(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.hashes=[]
        self.hashes.extend(list(hashlib.algorithms_available))

    def dinb(self,s):
        return int(s,2)

    def bind(self,s):
        s=s.replace(' ','')
        r=''
        for i in range(0,len(s),7):
            r+=chr(self.dinb(s[i:i+7]))
        return r

    @group(name='devtools',aliases=['dt'],invoke_without_command=True)
    async def devtools_grp(self,ctx):
        await ctx.send("INDEV DEVTOOLS GRP")

    @devtools_grp.command(name='hash')
    async def hash_command(self,ctx,mode:Optional[str]='sha256',*,inps:Optional[str]='hello world'):
        try:
            r=eval("".join(['hashlib.',mode,'(',"b'",inps,"'",')','.hexdigest()']))
        except Exception as e:
            print(e)
            r="Couldn't Hash in {}".format(mode)
        em=Embed(
            title='**`{} Hash`**'.format(mode.upper()),
            description="```\"{}\"s {} Hash\n{}```".format(inps,mode,r),
            color=Color.from_rgb(0,0,0)
        )
        await ctx.send(embed=em)

    @devtools_grp.group(name='binary',aliases=['bin'],invoke_without_command=True)
    async def binary_grp(self,ctx):
        await ctx.send("INDEV BINARY GRP")

    @binary_grp.command(name='encode',aliases=['enc','en'])
    async def encode_binary(self,ctx,*,string:Optional[str]='hello world'):
        e=' '.join('{0:08b}'.format(ord(x), 'b') for x in string)
        print(e,type(e))
        em=Embed(
            title='**`Binary Encoding`**',
            description='```{} ->\n{}```'.format(string,e),
            color=Color.from_rgb(0,0,0)
        )
        await ctx.send(embed=em)

    @binary_grp.command(name='decode',aliases=['dec','de'])
    async def decode_binary(self,ctx,*,string:Optional[str]='01101000 01100101 01101100 01101100 01101111'):
        em=Embed(
            title='**`Binary Decoding`**',
            description='```{} ->\n{}```'.format(string, self.bind(string)),
            color=Color.from_rgb(0,0,0)
        )
        await ctx.send(embed=em)

    @devtools_grp.group(name='hex',invoke_without_command=True)
    async def hex_grp(self,ctx):
        await ctx.send("INDEX HEX GRP")

    @hex_grp.command(name='encode',aliases=['enc','en'])
    async def encode_hex(self,ctx,*,string:Optional[str]='hello world'):
        h=''
        for i in string:
            h+=hex(ord(i)).lstrip('0x').rstrip('L')
        em=Embed(
            title='**`Hex Encoding`**',
            description='```{} ->\n{}```'.format(string,h),
            color=Color.from_rgb(0,0,0)
        )
        await ctx.send(embed=em)

    @hex_grp.command(name='decode',aliases=['dec','de'])
    async def decode_hex(self,ctx,*,string:Optional[str]=''):
        em=Embed(
            title='**`Hex Decoding`**',
            description='```{} ->\n{}```'.format(string,bytearray.fromhex(string).decode()),
            color=Color.from_rgb(0,0,0)
        )
        await ctx.send(embed=em)
    
def setup(bot):
    bot.add_cog(DEVTOOLS(bot))