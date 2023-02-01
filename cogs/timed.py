
from contextlib import closing
import random
import os
import string
import disnake
from PIL import Image, ImageFont, ImageDraw
from disnake.ext import commands
from disnake.ext.commands import has_permissions
import asyncio
import sys
from disnake.ext import tasks
import psycopg2



from config import password, host, db_name, bid

from config import user as userr

def pidor():
    def predicate(ctx):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT id FROM ban WHERE id = {ctx.author.id}")
                if c.fetchone() is not None:
                    return False
                else:
                    return True
    return commands.check(predicate)



'''

y: int = len(bot.guilds)

for n in range(0, y):

    g = [server.id for server in bot.guilds]
    a = n
    server = bot.get_guild(g[a])
    c.execute(f"SELECT id FROM server WHERE id = {server.id}")

    if c.fetchone() is None:
        print(f"В БД добавлен новый сервер - {server.name}")
        c.execute(f"INSERT INTO server (id, zarplatach1, zarplatach2, name) VALUES (%s, %s, %s, %s)", (server.id, None, None, server.name))
        
        db.commit()
    c.execute(f"SELECT serverid FROM guild WHERE serverid = {server.id}")

    if c.fetchone() is None:
        print(f"В БД добавлен новый сервер - {server.name}")
        c.execute(f"INSERT INTO guild (serverid, maxwarns, warnschannel, min) VALUES (%s, %s, %s, %s)", (server.id, None, None, None))
        
        db.commit()

    c.execute(f"SELECT serverid FROM language WHERE serverid = {server.id}")

    if c.fetchone() is None:
        c.execute(f"INSERT INTO language (serverid, lang) VALUES (%s, %s)", (server.id, None))
        db.commit()


    for member in server.members:  

        c.execute(f"SELECT userid, serverid FROM users WHERE userid = {member.id} AND serverid = {member.guild.id}")


        if c.fetchone() is None:
            if not member.bot:
                
                print(f"В БД добавлен новый пользователь - {member.name}, из {member.guild.name}")
                
                c.execute(f"INSERT INTO users (userid, serverid, nickname, mention, balance, bank, rep) VALUES (%s, %s, %s, %s, %s, %s, %s)", (member.id, member.guild.id, member.name, f'<@!{member.id}>', 0, 0, 0))



        db.commit()'''





class timed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statusb.stop()
        self.statusb.start()


    
    
    @commands.Cog.listener()
    async def on_ready(self):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:

        
                e = '\n'.join([str(f"{server} - {str(server.id)} - {str(len(server.members))}") for server in self.bot.guilds])
                print(f"Сейчас на {len(self.bot.guilds)} \n" + e + "\n")
                # Создание таблицы
                c.execute("""CREATE TABLE IF NOT EXISTS heck (
                        id  NUMERIC
                    )""")
                c.execute("""CREATE TABLE IF NOT EXISTS premium (
                        id  NUMERIC,
                        pass TEXT
                    )""")
                c.execute("""CREATE TABLE IF NOT EXISTS bannedg (
                        serverid  NUMERIC,
                        reason TEXT,
                        serveridown NUMERIC
                    )""")
                c.execute("""CREATE TABLE IF NOT EXISTS banned (
                        serverid  NUMERIC,
                        reason TEXT ,
                        memberid NUMERIC
                    )""")

                c.execute("""CREATE TABLE IF NOT EXISTS guild (
                        serverid  NUMERIC,
                        enabled TEXT,
                        serveridtu NUMERIC,
                        chnlid NUMERIC,
                        sandwc NUMERIC,
                        watermc NUMERIC,
                        gifton TEXT
                    )""")


                c.execute("""CREATE TABLE IF NOT EXISTS jopa (
                        serverid  NUMERIC,
                        channelid NUMERIC,
                        memberid NUMERIC
                    )""")

                c.execute("""CREATE TABLE IF NOT EXISTS piska (
                        serverid  NUMERIC,
                        channelid NUMERIC,
                        mani NUMERIC
                    )""")

                c.execute("""CREATE TABLE IF NOT EXISTS casino (
                        serverid  NUMERIC,
                        channelid NUMERIC
                    )""")


                c.execute("""CREATE TABLE IF NOT EXISTS bankomat (
                        serverid  NUMERIC,
                        channelid NUMERIC
                    )""")

                c.execute("""CREATE TABLE IF NOT EXISTS server (
                        id  NUMERIC,
                        zarplatach1 NUMERIC,
                        zarplatach2 NUMERIC,
                        name TEXT,
                        heckjopa TEXT
                    )""")

                c.execute("""CREATE TABLE IF NOT EXISTS shop (
                    roleid  NUMERIC,
                    serverid NUMERIC,
                    cost NUMERIC
                )""")

                c.execute("""CREATE TABLE IF NOT EXISTS users (
                    userid NUMERIC,
                    serverid NUMERIC,
                    nickname TEXT,
                    mention TEXT,
                    balance NUMERIC,
                    bank NUMERIC,
                    rep NUMERIC,
                    counter NUMERIC,
                    lvl NUMERIC,
                    sandw NUMERIC,
                    waterm NUMERIC,
                    lastmes TEXT
                )""")
                db.commit()


    '''@commands.slash_command(name="work", dm_permission=False)  # Экономика
    @commands.cooldown(1, 43200, commands.BucketType.member)
    async def ___work(self, inter: disnake.ApplicationCommandInteraction):
        """[Экономика] - Работать (Радиус зарплаты определябт админы)"""
        c.execute(f"SELECT zarplatach1 FROM server WHERE id = {inter.guild.id}")
        if c.fetchone()[0] is None:
            await inter.response.send_message("Не установлен лимит зарплаты!")
            self.___work.reset_cooldown(inter)
            return
        c.execute(f"SELECT bank FROM users WHERE userid = {inter.author.id} AND serverid = {inter.guild.id}")
        do = c.fetchone()[0]
        c.execute(f"SELECT zarplatach1 FROM server WHERE id = {inter.guild.id}")
        one = c.fetchone()[0]
        c.execute(f"SELECT zarplatach2 FROM server WHERE id = {inter.guild.id}")
        two = c.fetchone()[0]
        rand: int = random.randint(int(one), int(two))
        c.execute(f"UPDATE users SET bank = bank + {rand} WHERE userid = {inter.author.id} AND serverid = {inter.guild.id}")
        db.commit()
        c.execute(f"SELECT bank FROM users WHERE userid = {inter.author.id} AND serverid = {inter.guild.id}")
        posle = c.fetchone()[0]
        embed = disnake.Embed(title="**ЗАРПЛАТА**",
                              description=f"Вы успешно заработали {rand}<:hdollar:1038118641176162394>!\n\nВаш баланс в банке до: {do}<:hdollar:1038118641176162394>\nВаш баланс в банке после: {posle}<:hdollar:1038118641176162394>\n\nВы можете поработать только через 12 часов!",
                              color=0x7000cc)
        await inter.response.send_message(embed=embed)'''

    @tasks.loop(minutes=30)
    async def statusb(self):
        chnl = self.bot.get_channel(1028772927144996903)


        await chnl.purge(limit=5)
        
        embed = disnake.Embed(title="**Статус**",
                                description=f"Пинг бота - {round(self.bot.latency * 1000)}мс\nКоличество серверов - {str(len(self.bot.guilds))}\nКоличество участников - {str(len(self.bot.users))}\n\nДанная статистика обновляется раз в 30 минут.",
                                color=0x7300ff)
        
        await chnl.send(embed=embed)




    
    @commands.command(aliases=["crime", "ограбить"])
    @commands.guild_only()
    @commands.cooldown(1, 300 , commands.BucketType.member)
    @pidor()
    async def __crime(self, ctx, target: disnake.Member = None):
        if ctx.guild.id == 1045030168944713879:
            await ctx.send("Команда заблокирована!")
            return
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if target is None:
                    await ctx.send("Вы не указали цель!")
                    return
                if target.bot:
                    await ctx.send("Это бот!")
                    return
                if ctx.author.id == target.id:
                    await ctx.send("Это вы!")
                    return
                if target not in ctx.guild.members:
                    await ctx.send("Я не могу найти данного пользователя!")
                    return
                o = random.randint(1, 3)
                if o != 1:
                    if o == 3:
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.author.id} AND serverid = {ctx.guild.id}")
                        bal = c.fetchone()[0]
                        c.execute(f"SELECT zarplatach1 FROM server WHERE id = {ctx.guild.id}")
                        otkup: int = int(c.fetchone()[0])*2
                        if bal >= otkup:
                            c.execute(f"UPDATE users SET balance = balance - {otkup} WHERE userid = {ctx.author.id} AND serverid = {ctx.guild.id}")
                            db.commit()
                            await ctx.send(f"Неподалеку была полиция, вас повязали и отвезли в участок. К счастью, вы смогли откупиться. Взятка составила {str(otkup)}<:hdollar:1038118641176162394>")
                        else:
                            c.execute(f"UPDATE users SET balance = 0 WHERE userid = {ctx.author.id} AND serverid = {ctx.guild.id}")
                            db.commit()
                            await ctx.send(f"Неподалеку была полиция, вас повязали и отвезли в участок. К сожалению, денег на взятку у вас не хватило, пришлось дополнительно поработать проституткой в отделении")
                    else:
                        abc = ['На вас слишком косо смотрели, вы решили этого не делать.', "У пользователя был перцовый баллончик..." , "У пользователя был нож... Вам пришлось удирать со скоростью звука."]
                        await ctx.send(random.choice(abc))
                        return
                else:
                    c.execute(f"SELECT balance FROM users WHERE userid = {target.id} AND serverid = {ctx.guild.id}")
                    if c.fetchone()[0] == 0:
                        abc = ['На вас слишком косо смотрели, вы решили этого не делать.', "У пользователя был перцовый баллончик..." , "У пользователя был нож... Вам пришлось удирать со скоростью звука."]
                        await ctx.send(random.choice(abc))
                        return
                    c.execute(f"SELECT balance FROM users WHERE userid = {target.id} AND serverid = {ctx.guild.id}")
                    if random.randint(1, 2) == 1:
                        bal = c.fetchone()[0]
                        plus = bal / 3 
                        plu: int = round(plus * 2)
                    else:
                        bal = c.fetchone()[0]
                        plu: int = round(bal / 3) 
                    c.execute(f"UPDATE users SET balance = balance - {plu} WHERE userid = {target.id} AND serverid = {ctx.guild.id}")
                    c.execute(f"UPDATE users SET balance = balance + {plu} WHERE userid = {ctx.author.id} AND serverid = {ctx.guild.id}")
                    db.commit()
                    await ctx.send(f"{ctx.author.mention}, ограбление удалось! Вам было начислено {str(plu)}<:hdollar:1038118641176162394>")

    @commands.command(aliases=["работать", "work"])  # Экономика
    @commands.cooldown(1, 43200, commands.BucketType.member)
    @commands.guild_only()
    @pidor()
    async def __work(self, ctx):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT zarplatach1 FROM server WHERE id = {ctx.guild.id}")
                if c.fetchone()[0] is None:
                    await ctx.send("Не установлен лимит зарплаты!")
                    self.__work.reset_cooldown(ctx)
                    return
                c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                do = c.fetchone()[0]
                c.execute(f"SELECT zarplatach1 FROM server WHERE id = {ctx.guild.id}")
                one = c.fetchone()[0]
                c.execute(f"SELECT zarplatach2 FROM server WHERE id = {ctx.guild.id}")
                two = c.fetchone()[0]
                rand: int = random.randint(int(one), int(two))
                c.execute(f"UPDATE users SET bank = bank + {rand} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                db.commit()
                c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                posle = c.fetchone()[0]
                embed = disnake.Embed(title="**ЗАРПЛАТА**",
                                    description=f"Вы успешно заработали {rand}<:hdollar:1038118641176162394>!\n\nВаш баланс в банке до: {do}<:hdollar:1038118641176162394>\nВаш баланс в банке после: {posle}<:hdollar:1038118641176162394>\n\nВы можете поработать только через 12 часов!",
                                    color=0x7000cc)
                await ctx.send(embed=embed)

    @commands.command(aliases=['+rep'])
    @commands.guild_only()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    @pidor()
    async def __vrep(self, ctx, usr: disnake.Member = None):
        if usr.id == ctx.message.author.id:
            await ctx.send("Вы не можете самому себе зачислить репутацию!")
            self.__vrep.reset_cooldown(ctx)
            return
        else:
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"UPDATE users SET rep = rep + 1 WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    db.commit()
                    c.execute(f"SELECT rep FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    rep = c.fetchone()[0]
                    await ctx.send(f"Вы добавили {usr.mention} одно очко репутации! Теперь у него(неё): {rep}!")

    @commands.command(aliases=['-rep'])
    @commands.guild_only()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    @pidor()
    async def __unrep(self, ctx, usr: disnake.Member):
        if usr.id == ctx.message.author.id:
            await ctx.send("Вы не можете самому себе снять репутацию!")
            self.__unrep.reset_cooldown(ctx)
            return
        else:
            if usr.bot:
                await ctx.send("Это бот!")
                self.__unrep.reset_cooldown(ctx)
                return
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"UPDATE users SET rep = rep - 1 WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    db.commit()
                    c.execute(f"SELECT rep FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    rep = c.fetchone()[0]
                    await ctx.send(f"Вы сняли {usr.mention} одно очко репутации! Теперь у него(неё): {rep}!")

    


    @commands.command(aliases=['muteall'])  # Из модерирования
    @has_permissions(administrator=True)
    @commands.guild_only()
    async def __muteall(self, ctx):
        role = disnake.utils.get(ctx.guild.roles, name="MUTE")

        if role in ctx.guild.roles:
            for member in ctx.guild.members:
                await member.add_roles(role)
                await ctx.send(f"Member {member.mention} has muted<a:yes:952255158992142417>")
        else:
            await ctx.guild.create_role(name="MUTE", permissions=disnake.Permissions(send_messages=False, speak=False, read_messages=True, read_message_history=True))
            for member in ctx.guild.members:
                role = disnake.utils.get(ctx.guild.roles, name="MUTE")
                await member.add_roles(role)
                await ctx.send(f"Member {member.mention} has muted<a:yes:952255158992142417>")


def setup(bot):
    bot.add_cog(timed(bot))
