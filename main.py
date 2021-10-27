#pip3 install -U git+https://github.com/nextcord/nextcord.git#master

from gevent import monkey as curious_george
curious_george.patch_all(thread=False,select=False)
from alpha_core.Bot.runner import Bot

def main():
    bot=Bot()
    bot.run()

main()
