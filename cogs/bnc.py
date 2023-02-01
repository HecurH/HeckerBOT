import sdc_api_py
from disnake.ext import commands
from main import bot

class BotsSDC(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):                       #Аргумент fork_name опциональный. Укажите название используемого форка discord.py если таковой используется.
                                                    #Название нужно указыать то, с помощью которого вы импортировали форк в свой проект.
        bots = sdc_api_py.Bots(self.bot, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk0NDg5MDE2Mzk3NTMyMzcyOCIsInBlcm1zIjowLCJpYXQiOjE2NDk5NjEyMTV9.GuR5-U3zc2HRX51Bub8eJ98N2t2g9l3fDmdDF_LJM3g", "disnake") # Аргумент logging опциональный. По умолчанию True.
        bots.create_loop(39)  #Как аргумент можно использовать время в минутах. Раз в это количество минут будет отправляться статистика.
   


def setup(bot):                            #По умолчанию 60 минут. Минимальный порог 30 минут.
    bot.add_cog(BotsSDC(bot))