import disnake
from disnake.ext import commands
from config import bid
import random
from boticordpy import BoticordClient
from main import bot


async def get_stats():
        return {"servers": len(bot.guilds), "shards": 2, "users": len(bot.users)}

async def on_error_posting(exception):
    print(exception)

async def on_success_posting():
    print("done")




class boticordpy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    


    boticord_client = BoticordClient("Bot 7710dcaf-cd1a-42b8-b015-c58f154c831e", version=2)
    autopost = (
        boticord_client.autopost()
        .init_stats(get_stats)
        .on_success(on_success_posting)
        .on_error(on_error_posting)
        .set_interval(1800)
        .start()
    )

def setup(bot):
    bot.add_cog(boticordpy(bot))
