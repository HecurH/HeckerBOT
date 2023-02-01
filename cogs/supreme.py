from contextlib import closing
import random
import string
import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions
import asyncio
import qrcode
import requests
import datetime
from disnake.ext import tasks
from datetime import timedelta, date

import subprocess
from rich.console import Console
from time import perf_counter, sleep
console = Console()
from config import password, host, db_name, bid

from config import user as userr
def shh():
    def predicate(ctx):
        if ctx.message.author.id not in bid:
            return False
        else:
            return True
    return commands.check(predicate)
import psycopg2



class supreme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command(name='чикель')
    @shh()
    async def __re(self, ctx):
        db1 = psycopg2.connect(host='localhost', user='serverss', password='123', database='hecker')
        c1 = db1.cursor()



        y: int = len(self.bot.guilds)




        for n in range(0, y):


            g = [server.id for server in self.bot.guilds]
            a = n
            server = self.bot.get_guild(g[a])

            print('Тест сервера "' + server.name + '"')
            if server.id != 971771931705630730:
                if server.id != 374071874222686211:

                    c1.execute(f"SELECT id FROM server WHERE id = {server.id}")

                    if c1.fetchone() is None:
                        print(f"В БД добавлен новый сервер - {server.name}")
                        c1.execute(f"INSERT INTO server (id, zarplatach1, zarplatach2, name, heckjopa) VALUES (%s, %s, %s, %s, %s)", (server.id, None, None, server.name, 'No'))
                        
                        db1.commit()

                    c1.execute(f"SELECT serverid FROM guild WHERE serverid = {server.id}")

                    if c1.fetchone() is None:
                        print(f"В БД добавлен новый сервер - {server.name}")
                        c1.execute(f"INSERT INTO guild (serverid, enabled, serveridtu, chnlid, sandwc, watermc, gifton) VALUES (%s, %s, %s, %s, %s, %s, %s)", (server.id, 'Disabled', 0, None, 2800, 9000, 'Disabled'))


                        db1.commit()


                    num=0
                    start = perf_counter()
                    for member in server.members:  # цикл, обрабатывающий список участников


                        

                        c1.execute(f"SELECT userid, serverid FROM users WHERE userid = {member.id} AND serverid = {member.guild.id}")


                        if c1.fetchone() is None:
                            if not member.bot:
                                num += 1
                                
                                console.log(f"[bold][green]- Добавлен участник #[/green]{num} [green]-[/green]")
                                print(member.name)
                                # вводит все данные об участнике в БД
                                c1.execute(f"INSERT INTO users (userid, serverid, nickname, mention, balance, bank, rep, counter, lvl, sandw, waterm, lastmes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (member.id, member.guild.id, member.name, f'<@!{member.id}>', 0, 0, 0, 0, 0, 0, 0, None))



                        db1.commit()  # применение изменений в БД
                    end = perf_counter()
                    print(end - start)

        c1.execute("SELECT userid FROM users")
        for id in c1.fetchall():
            if self.bot.get_user(id[0]) is None:
                print("кто-то удален")
                c1.execute(f"DELETE FROM users WHERE userid = {id[0]}")
                db1.commit




        print("work end")
        c1.close()
        db1.close()

     
    @commands.command(name='акт')
    @shh()
    async def __res(self, ctx):
        self.premis.start()
    @commands.command(name='диз')
    @shh()
    async def __ref(self, ctx):
        self.premis.stop()



    @commands.command(name='прем')
    @shh()
    async def __prem(self, ctx):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
        
                embed = disnake.Embed(title="**Узбек**", color=0x7000cc, timestamp=ctx.message.created_at)
                counter = 0
                c.execute("SELECT id FROM premium")
                a = c.fetchall()
                for n in a:
                    counter += 1
                    usr = self.bot.get_user(n[0])
                    if usr is None:
                        embed.add_field(
                            name=f"** **",
                            value=f"{counter}# | {n[0]} (Нет такого узера)",
                            inline=False)
                    else:
                        embed.add_field(
                            name=f"** **",
                            value=f"{counter}# | {usr.name}",
                            inline=False)
                await ctx.send(embed=embed)

    @tasks.loop(minutes=1)
    async def premis(self):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute("SELECT id FROM premium")
                for usr in c.fetchall():
                    usrid = usr[0]
                    c.execute(f"SELECT tsend FROM premium WHERE id = {usrid}")
                    usrtsend = c.fetchone()[0]
                    now = datetime.datetime.now()
                    tsnow = now.timestamp()
                    if tsnow >= usrtsend:
                        c.execute(f"DELETE FROM premium WHERE id = {usrid}")
                        db.commit()
                        mem = self.bot.get_guild(844649033502818314).get_member(usrid)
                        if mem is not None:
                            role = self.bot.get_guild(844649033502818314).get_role(1037770212004605972)
                            await mem.remove_roles(role)
                        usrr = self.bot.get_user(usrid)
                        if usrr is not None:
                            await usrr.send(f"Здравствуйте! Ваш премиум истек.")

        

    @commands.command(name='+прем')
    @shh()
    async def __addprem(self, ctx, id:int):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                usr = self.bot.get_user(id)
                c.execute(f"SELECT id FROM premium WHERE id = {int(id)}")
                if c.fetchone() is not None:
                    await ctx.send("Данный пользователь уже в БД!")
                    return
                if usr not in self.bot.users:
                    await ctx.send("Я не могу найти этого пользователя!")
                    return
                if usr.bot:
                    await ctx.send("Это бот!")
                    return


                pas = ''
                for x in range(8): #Количество символов (16)
                    pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
                now = datetime.datetime.now()
                tsnow = now.timestamp()
                tse = now + datetime.timedelta(days=30)
                tsend = tse.timestamp()
                c.execute("INSERT INTO premium (id, pass, tsnow, tsend) VALUES (%s, %s, %s, %s)", (id, f'{pas}', tsnow, tsend))
                db.commit()
                mem = self.bot.get_guild(844649033502818314).get_member(id)
                if mem is not None:
                    role = self.bot.get_guild(844649033502818314).get_role(1037770212004605972)
                    await mem.add_roles(role)
                await ctx.send("Успешно!")
                usr = self.bot.get_user(id)
                await usr.send(f"Здравствуйте! Вам был выдан премиум для бота heckerBOT, поздравляю!\nВаш пароль для доступа к sudo-командам - {str(pas)}. Премиум истечет <t:{round(tsend)}:R>")
    @commands.command(name='-прем')
    @shh()
    async def __remprem(self, ctx, id:int):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                usr = self.bot.get_user(id)
                c.execute(f"SELECT id FROM premium WHERE id = {int(id)}")
                if c.fetchone() is None:
                    await ctx.send("Данный пользователь не в БД!")
                    return

                c.execute(f"DELETE FROM premium WHERE id = {id}")
                db.commit()
                mem = self.bot.get_guild(844649033502818314).get_member(id)
                if mem is not None:
                    role = self.bot.get_guild(844649033502818314).get_role(1037770212004605972)
                    await mem.remove_roles(role)
                await ctx.send("Успешно!")

                usr = self.bot.get_user(id)
                if usr is not None:
                    await usr.send(f"Здравствуйте! Ваш премиум был удален.")














def setup(bot):
    bot.add_cog(supreme(bot))
