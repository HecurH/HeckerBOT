from config import user, password, host, db_name, token, bid
import psycopg2
import disnake
from disnake.ext import commands

from time import perf_counter
import topgg
from disnake.ext import commands, tasks
import os
import discordspy as discordspy
from boticordpy import webhook



intents = disnake.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.all()

bot = commands.AutoShardedBot(shard_count=2, command_prefix='*', case_insensitive=True,
                   help_command=None, intents=intents, activity=disnake.Game(name="*помощь"), status = disnake.Status.idle, sync_commands_debug=True)
dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk0NDg5MDE2Mzk3NTMyMzcyOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjQ5MDg4MTU5fQ.S2pR-2G60oHBE6eM0etTn6AXcrF1I49ay7TaGn4f0xQ"
bot.topggpy = topgg.DBLClient(bot, dbl_token)




@tasks.loop(minutes=30)
async def update_stats():
    """This function runs every 30 minutes to automatically update your server count."""
    try:
        await bot.topggpy.post_guild_count()
        print(f"Posted server count ({bot.topggpy.guild_count})")
    except Exception as e:
        print(f"Failed to post server count")



@bot.command()
async def invi(ctx, server_id: int):
    if ctx.message.author.id not in bid:
        return
    guild = bot.get_guild(server_id)
    invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=2, temporary=False)
    await ctx.send(f"https://discord.gg/{invite.code}")




@bot.command()  # Стандартное объявление комманды
async def load(ctx, extension):  # объявление функции
    if ctx.message.author.id not in bid:
        return
    bot.load_extension(f'cogs.{extension}')  # загрузка доплонений
    await ctx.send('Ког загружен!')


@bot.command()
async def unload(ctx, extension):
    if ctx.message.author.id not in bid:
        return
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send('Ког выгружен!')


@bot.command()
async def reload(ctx, extension):
    if ctx.message.author.id not in bid:
        return

    bot.unload_extension(f'cogs.{extension}')  # отгружаем ког
    bot.load_extension(f'cogs.{extension}')  # загружаем

    await ctx.send('Ког перезагружен!')




for filename in os.listdir('./cogs'):  # Цикл перебирающий файлы в cogs
    if filename.endswith('.py'):  # если файл кончается на .py, то это наш ког
        start = perf_counter()
        bot.load_extension(f'cogs.{filename[:-3]}')
        end = perf_counter()
        print(end - start)

async def test_webhook_message(data):
    print(data)


boticord_webhook = webhook.Webhook("e6e4255408f84e16", "/bot").register_listener(
    "test_webhook_message", test_webhook_message)
boticord_webhook.start(5000)


bot.run(token)
