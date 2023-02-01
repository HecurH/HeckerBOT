import asyncio
from asyncio import exceptions, TimeoutError
import disnake
from disnake.ext import commands
from config import bid
import random
import math
import psycopg2
from configsrv import host, user, password, db_name
from rich.console import Console
from time import sleep
from rich.markdown import Markdown

console = Console()

from time import perf_counter


class servernew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def stop(self, ctx):
        if ctx.message.author.id not in bid:
            return

        
        raise SystemExit(0)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        c = db.cursor()
        

        sumas = []
        with console.status("[bold blue]Добавляем сервер в БД...") as status:

            c.execute(f"INSERT INTO server (id, zarplatach1, zarplatach2, name, heckjopa) VALUES (%s, %s, %s, %s, %s)", (guild.id, None, None, guild.name, 'No'))
            c.execute(f"INSERT INTO guild (serverid, enabled, serveridtu, chnlid, sandwc, watermc, gifton) VALUES (%s, %s, %s, %s, %s, %s, %s)", (guild.id, 'Disabled', 0, None, 2800, 9000, 'Disabled'))
            db.commit()
            console.log(f'[bold][blue]Добавлен сервер -[/blue] {guild.name}')
            num = 0
            for member in guild.members:  # цикл, обрабатывающий список участников

                
                if not member.bot:
                    start1 = perf_counter()

                    # вводит все данные об участнике в БД
                    c.execute(f"INSERT INTO users (userid, serverid, nickname, mention, balance, bank, rep, counter, lvl, sandw, waterm, lastmes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (member.id, member.guild.id, member.name, f'<@!{member.id}>', 0, 0, 0, 0, 0, 0, 0, None))  # вводит все данные об участнике в БД

                    db.commit()  # применение изменений в БД
                    num += 1
                    console.log(f"[bold][green]- Добавлен участник #[/green]{num} [green]-[/green] {member.name}")
                    end1 = perf_counter()
                    sumas.append(end1 - start1)
        

        console.log(f'[bold][green]Готово! Общее время добавления - {str(sum(sumas))}, общее время добавления участиника - {str(sum(sumas) / len(sumas))}')
                    
        channel = self.bot.get_channel(844942954800087101)

        await channel.send("Новый сервер! '" + str(guild) + "'" + ' ' + str(guild.id))
        

        channel = guild.text_channels[0]

        embed = disnake.Embed(title="**Привет!**",
                              description='Спасибо что добавили меня на свой сервер!\n\n\nЕсли что, список команд доступен по "*помощь"',
                              color=0x5900ff)
        embed.set_author(name="heckerBOT", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                         icon_url="https://cdn.discordapp.com/avatars/944890163975323728/36416ec401ad36dde8ddf01d2c1af9cc.png?size=256")
        try:
            await channel.send(embed=embed)
        except:
            a = guild.owner
            embedd = disnake.Embed(title="**Привет!**",
                              description='Спасибо что добавили меня на свой сервер!\n\n\nЕсли что, список команд доступен по "*помощь" \nУ меня не вышло написать в канал',
                              color=0x5900ff)
            embedd.set_author(name="heckerBOT", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                         icon_url="https://cdn.discordapp.com/avatars/944890163975323728/36416ec401ad36dde8ddf01d2c1af9cc.png?size=256")
            await a.send(embed=embedd)
        c.close()
        db.close()




def setup(bot):
    bot.add_cog(servernew(bot))
