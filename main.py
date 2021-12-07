#pip3 install -U git+https://github.com/nextcord/nextcord.git#master -- Nextcord

from gevent import monkey as very_curious_george
very_curious_george.patch_all(thread=False,select=False)
from core.Bot.runner import Bot

def main():
    bot=Bot()
    bot.run()

main()
