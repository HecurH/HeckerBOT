
from contextlib import closing
import math
import random
import os
import string
import disnake
from PIL import Image, ImageFont, ImageDraw
from disnake.ext import commands
from disnake.ext.commands import has_permissions
import asyncio
import psycopg2
from rich.console import Console
from rich.table import Table
from disnake.enums import ButtonStyle
from config import password, host, db_name, bid
class one(disnake.ui.View):
    msg: disnake.Message
    
    def __init__(self, ctx):
        super().__init__(timeout=100)
        self.ctx = ctx




    async def interaction_check(self, interaction: disnake.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Вы не автор команды!", ephemeral=True)
            return False
        else:
            return True
    async def on_timeout(self):
        self.children[0].disabled = True  # type: ignore
        self.children[1].disabled = True  # type: ignore
        try:
            await self.msg.edit(view=self)
        except:
            pass
        self.stop()

    @disnake.ui.button(label="1 роль", style=ButtonStyle.red, row=1)
    async def fi(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        return
    @disnake.ui.button(label="2 роль", style=ButtonStyle.red, row=1)
    async def fir(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        return
    @disnake.ui.button(label="3 роль", style=ButtonStyle.blurple, row=2)
    async def firs(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        return
    @disnake.ui.button(label="4 роль", style=ButtonStyle.blurple, row=2)
    async def first_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        return
    @disnake.ui.button(label="5 роль", style=ButtonStyle.green, row=3)
    async def first_b(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        return
    @disnake.ui.button(label="6 роль", style=ButtonStyle.green, row=3)
    async def first_bu(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        return


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

from config import user as userr
def add_money(bott, id: int, money: int, bank: bool, ctx):
    with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
        with db.cursor() as c:
            if int(money) < 1:
                    
                return False
            if id is None:
                return False
            if bott.get_user(id) is None:
                return False
            if bank is False:
                usr = bott.get_user(id)
                c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                balance = c.fetchone()
                if balance is None:
                    return False
                c.execute(f"UPDATE users SET balance = balance + {money} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                db.commit()
                return True
            if bank is True:
                usr = bott.get_user(id)
                c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                bank = c.fetchone()
                if bank is None:
                    return False
                c.execute(f"UPDATE users SET bank = bank + {money} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                db.commit()
                return True

class eko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def aab(self, ctx):
        view = one(ctx)
        await ctx.send("Тут типо список ролей, нажмите на кнопку чтобы купить", view=view)
        

    @commands.command(aliases=["casino", "казино"])
    @commands.guild_only()
    @pidor()
    async def __casino(self, ctx, suma: int = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT serverid, channelid FROM casino WHERE serverid = {ctx.guild.id} AND channelid = {ctx.channel.id}")
                if c.fetchone() is None:
                    await ctx.send("В данном канале не установлено казино!<:onno:954815596082659368>")
                    return
                if suma is None:
                    await ctx.send("Вы не указали ставку!")
                    return
                elif suma < 10:
                    await ctx.send("Минимальная ставка 10<:hdollar:1038118641176162394>!")
                    return

                c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")    
                if suma > c.fetchone()[0]:
                    await ctx.send("У вас недостаточно средств!")
                    return
                else:


                    embed = disnake.Embed(title="**КАЗИНО**", description="Я загадаю число от 1 до 20, если вы его угадываете, то приумножите свой капитал в 5 раз. Если загаданное число четное, а ваше число тоже четное, то вы получите X2.", color=0x7000cc)

                    await ctx.send(embed=embed)
                    await ctx.send("Если вы согласны с условиями игры и своей ставкой, напишите 'Да', иначе - 'Нет'")
                    def check(m):
                        return m.channel == ctx.channel and m.author == ctx.author

                    message1 = await self.bot.wait_for('message', check=check, timeout=60)
                    yep = ["y", "yes", "д", "да"]
                    if message1.content.lower() not in yep:
                        await ctx.send("Отменил игру.")
                        return



                    s = await ctx.send("Загадываю")
                    await s.edit(content=f"Загадываю.")
                    await s.edit(content=f"Загадываю..")
                    await s.edit(content=f"Загадываю...")
                    await s.edit(content=f"Загадываю.")
                    await s.edit(content=f"Загадываю..")
                    await s.edit(content=f"Загадываю...")
                    a: int = random.randint(1, 20)
                    print(a)
                    await ctx.send("Число загадано, введите число:")
                    message = await self.bot.wait_for('message', check=check, timeout=60)
                    ass: int = message.content
                    if int(ass) < 1:
                        await ctx.send("Дядь, ты тютю?")
                        return
                    if int(ass) == int(a):

                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        do = c.fetchone()[0]
                        asss: int = suma * 5
                        c.execute(f"UPDATE users SET balance = balance - {suma} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        c.execute(f"UPDATE users SET balance = balance + {asss} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        posle = c.fetchone()[0]


                        embed=disnake.Embed(title="**УРА, ВЫИГРЫШ**", description=f"Вы приумножили свой капитал в 5 раз ({asss}<:hdollar:1038118641176162394>)\n\nВаши наличные до пополнения: {do}<:hdollar:1038118641176162394>\nВаши наличные после пополнения: {posle}<:hdollar:1038118641176162394>", color=0x00ff0a)
                        await ctx.send(embed=embed)

                    elif (int(a) % 2) == 0:
                        if (int(ass) % 2) == 0:

                            c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                            do = c.fetchone()[0]
                            asss: int = suma * 2
                            c.execute(f"UPDATE users SET balance = balance - {suma} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                            c.execute(f"UPDATE users SET balance = balance + {asss} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                            db.commit()
                            c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                            posle = c.fetchone()[0]


                            embed=disnake.Embed(title="**ВЫИГРЫШ?**", description=f"Вы приумножили свой капитал в 2 раза ({asss}<:hdollar:1038118641176162394>)\n\nВаши наличные до пополнения: {do}<:hdollar:1038118641176162394>\nВаши наличные после пополнения: {posle}<:hdollar:1038118641176162394>", color=0x00ff0a)
                            await ctx.send(embed=embed)
                        else:
                            c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                            do = c.fetchone()[0]
                            c.execute(f"UPDATE users SET balance = balance - {suma} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                            db.commit()
                            c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                            posle = c.fetchone()[0]

                            embed = disnake.Embed(title="**ПРОИГРЫШ**", description=f"Вы проиграли\n\nВаши наличные до: {do}<:hdollar:1038118641176162394>\nВаши наличные после: {posle}<:hdollar:1038118641176162394>", color=0xff0000)
                            await ctx.send(embed=embed)

                    else:
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        do = c.fetchone()[0]
                        c.execute(f"UPDATE users SET balance = balance - {suma} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        posle = c.fetchone()[0]


                        embed = disnake.Embed(title="**ПРОИГРЫШ**", description=f"Вы проиграли\n\nВаши наличные до: {do}<:hdollar:1038118641176162394>\nВаши наличные после: {posle}<:hdollar:1038118641176162394>", color=0xff0000)
                        await ctx.send(embed=embed)


                
                


    @commands.command(aliases=["set_work", 'зарплата'])
    @has_permissions(administrator=True)
    @commands.guild_only()
    @pidor()
    async def __set_work(self, ctx, one: int, two: int):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT zarplatach1 FROM server WHERE id = {ctx.guild.id}")
                if c.fetchone()[0] is None:
                    if one > two:
                        await ctx.send("Первое число не может быть больше второго!")
                        return
                    c.execute(f"UPDATE server SET zarplatach1 = {one} WHERE id = {ctx.guild.id}")
                    c.execute(f"UPDATE server SET zarplatach2 = {two} WHERE id = {ctx.guild.id}")
                    db.commit()
                    embed = disnake.Embed(title="**ЛИМИТ ЗАРАБОТНОЙ ПЛАТЫ**",
                                        description=f"Вы упешно установили лимит на:\n\nОт {one}<:hdollar:1038118641176162394>, до {two}<:hdollar:1038118641176162394>", color=0x7000cc)
                    await ctx.send(embed=embed)
                else:
                    if one > two:
                        await ctx.send("Первое число не может быть больше второго!")
                        return
                    c.execute(f"UPDATE server SET zarplatach1 = {one} WHERE id = {ctx.guild.id}")
                    c.execute(f"UPDATE server SET zarplatach2 = {two} WHERE id = {ctx.guild.id}")
                    db.commit()
                    embed = disnake.Embed(title="**ЛИМИТ ЗАРАБОТНОЙ ПЛАТЫ**",
                                        description=f"Вы упешно изменили лимит на:\n\nОт {one}<:hdollar:1038118641176162394>, до {two}<:hdollar:1038118641176162394>",
                                        color=0x7000cc)
                    await ctx.send(embed=embed)

    @commands.command(aliases=["add_shop", 'add_role'])
    @has_permissions(administrator=True)
    @commands.guild_only()
    @pidor()
    async def __add_shop(self, ctx, role: disnake.Role = None, suma: int = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if role is None:
                    await ctx.send("Вы не указали роль!")
                    return
                elif suma is None:
                    await ctx.send("Вы не указали цену!")
                    return
                elif suma < 1:
                    await ctx.send("Нельзя указать цену меньше одного!")
                    return
                

                c.execute(f"SELECT roleid FROM shop WHERE roleid = {role.id} AND serverid = {ctx.guild.id}")
                if c.fetchone() is None:
                    c.execute(f"INSERT INTO shop (roleid, serverid, cost) VALUES (%s, %s, %s)", (role.id, ctx.guild.id, suma))
                    db.commit()
                    await ctx.message.add_reaction("<a:yees:952255158992142417>")
                    await ctx.send("В магазин была добавлена новая роль, " + role.mention)
                    

                else:
                    await ctx.send("Роль уже в магазине!")
                    return

    @commands.command(aliases=['remove_shop', "remove_role"])
    @has_permissions(administrator=True)
    @commands.guild_only()
    @pidor()
    async def __remove_shop(self, ctx, role: disnake.Role = None):
        if role is None:
            await ctx.send("Укажите роль!")
            return
        else:
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT roleid FROM shop WHERE roleid = {role.id} AND serverid = {ctx.guild.id}")
                    if c.fetchone() is None:
                        await ctx.send("Мне нечего удалять")
                        return
                    else:
                        c.execute(f"DELETE FROM shop WHERE roleid = {role.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        await ctx.message.add_reaction("<a:yees:952255158992142417>")
                        await ctx.send("Из магазина была удалена роль, " + role.mention)

    @commands.command(aliases=["магазинн", "shopp"])
    @commands.guild_only()
    @pidor()
    async def __shopp(self, ctx):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                embed = disnake.Embed(title="**МАГАЗИН**", color=0x7000cc, timestamp=ctx.message.created_at)
                c.execute(f"SELECT serverid FROM shop WHERE serverid = {ctx.guild.id}")

                if c.fetchone() is None:
                    await ctx.send("В магазине нет ролей!")
                    return
                else:
                    c.execute(f"SELECT roleid FROM shop WHERE serverid = {ctx.guild.id}")

                    table = Table(title="МАГАЗИН")

                    table.add_column("Цена", style="cyan", no_wrap=True)
                    table.add_column("Роль", style="magenta")
                    for n in c.fetchall():
                        if ctx.guild.get_role(n[0]) is not None:
                            c.execute(f"SELECT cost FROM shop WHERE serverid = {ctx.guild.id} AND roleid = {n[0]}")

                            table.add_row(f"{c.fetchone()[0]}<:hdollar:1038118641176162394>", f"{ctx.guild.get_role(n[0]).mention}")
                    console = Console()

                    await ctx.send(console(table))

    @commands.command(aliases=["магазин", "shop"])
    @commands.guild_only()
    @pidor()
    async def __shop(self, ctx):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                embed = disnake.Embed(title="**МАГАЗИН**", color=0x7000cc, timestamp=ctx.message.created_at)
                c.execute(f"SELECT serverid FROM shop WHERE serverid = {ctx.guild.id}")
                cc = 0

                if c.fetchone() is None:
                    await ctx.send("В магазине нет ролей!")
                    return
                else:
                    c.execute(f"SELECT roleid FROM shop WHERE serverid = {ctx.guild.id}")
                    for n in c.fetchall():
                        if ctx.guild.get_role(n[0]) is not None:
                            cc += 1
                            embed.add_field(
                                name=f"** **",
                                value=f"{str(cc)}. {ctx.guild.get_role(n[0]).mention}, ",
                                inline=False
                            )
                            c.execute(f"SELECT cost FROM shop WHERE serverid = {ctx.guild.id} AND roleid = {n[0]}")
                            embed.add_field(
                                name=f"Стоимость: {c.fetchone()[0]}<:hdollar:1038118641176162394>;\n\n",
                                value=f"** **",
                                inline=False
                            )
                    await ctx.send(embed=embed)

    @commands.command(aliases=['rep'])
    @commands.guild_only()
    @pidor()
    async def __rep(self, ctx, usr: disnake.Member = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if usr == None:
                    c.execute(f"SELECT rep FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    rep = c.fetchone()[0]
                    embed = disnake.Embed(title="**РЕПУТАЦИЯ**",
                                        description=f"<@!{ctx.message.author.id}>, у вас {rep} очков репутации!",
                                        color=0x00ff04,
                                        timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)
                    return
                if not usr.bot:

                    c.execute(f"SELECT rep FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    rep = c.fetchone()[0]

                    embed = disnake.Embed(title="**РЕПУТАЦИЯ**",
                                        description=f"<@!{ctx.message.author.id}>, у {usr.mention} {rep} очков репутации!",
                                        color=0x00ff04,
                                        timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send("Это бот!")

    @commands.command(aliases=["купить", "buy"])
    @commands.guild_only()
    @pidor()
    async def __buy(self, ctx, num: int = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if num is None:
                    await ctx.send("Вы не указали роль!")
                    return
                if num < 1:
                    await ctx.send("Неа")
                    return
                num = num-1
                c.execute(f"SELECT roleid FROM shop WHERE serverid = {ctx.guild.id}")
                list = c.fetchall()
                iid = list[num]
                a = disnake.utils.get(ctx.guild.roles, id=iid[0])
                if a is None:
                    await ctx.send("Такой роли нет на сервере! Она будет удалена из списка ролей.")
                    c.execute(f"DELETE FROM shop WHERE roleid = {iid[0]} AND serverid = {ctx.guild.id}")
                    db.commit()
                    return
                if a in ctx.author.roles:
                    await ctx.send("У вас уже есть эта роль!")
                    return

                c.execute(f"SELECT cost FROM shop WHERE roleid = {a.id} AND serverid = {ctx.guild.id}")
                b = c.fetchone()[0]
                c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                if b > c.fetchone()[0]:
                    await ctx.send("На вашем счете недостаточно средств!")
                    return
                else:
                    c.execute(f"SELECT cost FROM shop WHERE roleid = {a.id} AND serverid = {ctx.guild.id}")
                    cost: int = c.fetchone()[0]
                    c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    do = c.fetchone()[0]

                    c.execute(f"UPDATE users SET balance = balance - {cost} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    db.commit()
                    await ctx.message.author.add_roles(a)
                    c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    posle = c.fetchone()[0]
                    embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ПОКУПКИ**",
                                        description=f"<@!{ctx.message.author.id}>, \n\nВы приобрели роль {a.mention} за {cost}<:hdollar:1038118641176162394>:\n\nВаш баланс до покупки: {do}<:hdollar:1038118641176162394>\nВаш баланс после: {posle}<:hdollar:1038118641176162394>",
                                        color=0x7000cc)
                    await ctx.send(embed=embed)

    @commands.command(aliases=["addcasino", "+казино"])
    @has_permissions(administrator=True)
    @commands.guild_only()
    @pidor()
    async def __casa(self, ctx, chnl: disnake.TextChannel = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if chnl is None:
                    chnl = self.bot.get_channel(ctx.message.channel.id)

                c.execute(f"SELECT channelid FROM casino WHERE serverid = {ctx.guild.id} AND channelid = {chnl.id}")
                if c.fetchone() is None:

                    c.execute(f"INSERT INTO casino (serverid, channelid) VALUES (%s, %s)", (ctx.guild.id, chnl.id))
                    db.commit()
                    await ctx.send(f"В канал {chnl.mention} успешно добавлено казино.<a:yes:952255158992142417>")
                else:
                    await ctx.send("В канале присутствует казино!")


    @commands.command(aliases=["remcasino", "-казино"])
    @has_permissions(administrator=True)
    @commands.guild_only()
    @pidor()
    async def __casb(self, ctx, chnl: disnake.TextChannel = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if chnl is None:
                    chnl = self.bot.get_channel(ctx.message.channel.id)
                
                c.execute(f"SELECT channelid FROM casino WHERE serverid = {int(ctx.guild.id)} AND channelid = {int(chnl.id)}")
                if c.fetchone() is None:
                    await ctx.send("В канале отсутствует банкомат!")
                else:
                    c.execute(f"DELETE FROM casino WHERE serverid = {ctx.guild.id} AND channelid = {chnl.id}")
                    db.commit()
                    await ctx.send(f"Из канала {chnl.mention} успешно демонтировано казино.<a:yes:952255158992142417>")


    @commands.command(aliases=["addatm", "+банк"])
    @has_permissions(administrator=True)
    @commands.guild_only()
    @pidor()
    async def __banka(self, ctx, chnl: disnake.TextChannel = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if chnl is None:
                    chnl = self.bot.get_channel(ctx.message.channel.id)

                c.execute(f"SELECT channelid FROM bankomat WHERE serverid = {ctx.guild.id} AND channelid = {chnl.id}")
                if c.fetchone() is None:

                    c.execute(f"INSERT INTO bankomat (serverid, channelid) VALUES (%s, %s)", (ctx.guild.id, chnl.id))
                    db.commit()
                    await ctx.send(f"В канал {chnl.mention} успешно добавлен банкомат.<a:yes:952255158992142417>")
                else:
                    await ctx.send("В канале присутствует банкомат!")

    @commands.command(aliases=["rematm", "-банк"])
    @has_permissions(administrator=True)
    @commands.guild_only()
    @pidor()
    async def __delb(self, ctx, chnl: disnake.TextChannel = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if chnl is None:
                    chnl = self.bot.get_channel(ctx.message.channel.id)

                c.execute(f"SELECT channelid FROM bankomat WHERE serverid = {int(ctx.guild.id)} AND channelid = {int(chnl.id)}")
                if c.fetchone() is None:
                    await ctx.send("В канале отсутствует банкомат!")
                else:
                    c.execute(f"DELETE FROM bankomat WHERE serverid = {ctx.guild.id} AND channelid = {chnl.id}")
                    db.commit()
                    await ctx.send(f"Из канала {chnl.mention} успешно демонтирован банкомат.<a:yes:952255158992142417>")

    @commands.command(aliases=["передать", "transfer"])
    @commands.guild_only()
    @pidor()
    async def __transfer(self, ctx, usr: disnake.Member = None, sum=None):
        if not usr.bot:
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    if sum is None:
                        await ctx.send("Вы не указали сумму!")
                        return

                    if usr is None:
                        await ctx.send("Вы не указали цель для перевода!")
                        return
                    else:
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        do_otp = c.fetchone()[0]
                        c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                        do_pol = c.fetchone()[0]

                        if int(sum) > int(do_otp):
                            await ctx.send("У вас недостаточно средств!")
                            return
                        else:
                            c.execute(f"UPDATE users SET balance = balance - {int(sum)} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")

                            c.execute(f"UPDATE users SET balance = balance + {int(sum)} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                            db.commit()
                            c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                            pos_otp = c.fetchone()[0]
                            c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                            pos_pol = c.fetchone()[0]

                            embed = disnake.Embed(title="**НАЛИЧНЫЕ ПОСЛЕ ПЕРЕЧИСЛЕНИЯ**",
                                                description=f"<@!{ctx.message.author.id}>, \n\nС вашего кармана было перечислено: {sum}<:hdollar:1038118641176162394>, на карман {usr.mention}\nВаш наличные до перечисления: {do_otp}<:hdollar:1038118641176162394>\nВаш наличные после: {pos_otp}<:hdollar:1038118641176162394>\n\nНаличные {usr.mention} до перечисления: {do_pol}<:hdollar:1038118641176162394>\nНаличные {usr.mention} после: {pos_pol}<:hdollar:1038118641176162394>",
                                                color=0x7000cc)
                            await ctx.send(embed=embed)
        else:
            await ctx.send("Это бот!")

    @commands.command(aliases=["аккаунт", "профиль", "account"])
    @commands.guild_only()
    @pidor()
    async def __acc(self, ctx, mem: disnake.Member = None):  # команда _account (где "_", ваш префикс указаный в начале)
        if mem is None:
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    bank = c.fetchone()[0]
                    c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    money = c.fetchone()[0]
                    c.execute(f"SELECT rep FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    inv = c.fetchone()[0]
                    myaccount = self.bot.get_user(ctx.message.author.id)
                    crea = f"год: {myaccount.created_at.year}, месяц: {myaccount.created_at.month}, день: {myaccount.created_at.day}, {myaccount.created_at.hour}:{myaccount.created_at.minute}"
                    embed = disnake.Embed(title="**АККАУНТ**",
                                        description=f"<@!{ctx.message.author.id}>, \n\nВаши наличные на данном сервере составляют: {money}<:hdollar:1038118641176162394>\nВаш баланс в банке составляет: {bank}<:hdollar:1038118641176162394>\nВаша репутация: {inv}\nАккаунт создан: {crea}",
                                        color=0x7000cc)
                    usr: disnake.User = ctx.message.author
                    embed.set_thumbnail(url=usr.avatar.url)
                    await ctx.send(embed=embed)

        else:
            if not mem.bot:
                with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                    with db.cursor() as c:
                        c.execute(f"SELECT bank FROM users WHERE userid = {mem.id} AND serverid = {ctx.guild.id}")
                        bank = c.fetchone()[0]
                        c.execute(f"SELECT balance FROM users WHERE userid = {mem.id} AND serverid = {ctx.guild.id}")
                        money = c.fetchone()[0]
                        c.execute(f"SELECT rep FROM users WHERE userid = {mem.id} AND serverid = {ctx.guild.id}")
                        inv = c.fetchone()[0]
                        myaccount = self.bot.get_user(mem.id)
                        crea = f"год: {myaccount.created_at.year}, месяц: {myaccount.created_at.month}, день: {myaccount.created_at.day}, {myaccount.created_at.hour}:{myaccount.created_at.minute}"

                        embed = disnake.Embed(title="**АККАУНТ**",
                                            description=f"<@!{mem.id}>, \n\nЕго наличные на данном сервере составляют: {money}<:hdollar:1038118641176162394>\nВаш баланс в банке составляет: {bank}<:hdollar:1038118641176162394>\nЕго репутация: {inv}\nАккаунт создан: {crea}",
                                            color=0x7000cc)
                        embed.set_thumbnail(url=mem.avatar.url)
                        await ctx.send(embed=embed)
            else:
                await ctx.send("Это бот!")

    @commands.command(aliases=["remove", "удалить"])
    @commands.guild_only()
    @has_permissions(administrator=True)
    @pidor()
    async def __remove(self, ctx, usr: disnake.Member = None, sum: int = None, shet=None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
        

                if not usr.bot:
                    if shet is None:
                        await ctx.send("Укажите в конце комманды счет. (банк или наличные)")
                    elif shet.lower() == "наличные":
                        if sum < 1:
                            await ctx.send("Нельзя так!")
                            return

                        c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                        do = int(c.fetchone()[0])
                        if sum == "all":
                            c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                            do = int(c.fetchone()[0])
                            c.execute(f"UPDATE users SET balance = 0 WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                            embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ СПИСАНИЯ**",
                                                description=f"<@!{usr.id}>, с вашего счета были списаны все деньги! \n\nCумма до снятия: {do}<:hdollar:1038118641176162394>\nСумма после снятия: 0<:hdollar:1038118641176162394>",
                                                color=0xff0000,
                                                timestamp=ctx.message.created_at)
                            await ctx.send(embed=embed)

                        c.execute(f"UPDATE users SET balance = balance - {int(sum)} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")

                        c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                        posle = int(c.fetchone()[0])

                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ СПИСАНИЯ**",
                                            description=f"С счета {usr.mention}, было списано: {sum}<:hdollar:1038118641176162394>\n\nCумма до снятия: {do}<:hdollar:1038118641176162394>\nСумма после снятия: {posle}<:hdollar:1038118641176162394>",
                                            color=0xff0000,
                                            timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)
                        db.commit()
                    elif shet.lower() == "банк":
                        if sum < 1:
                            await ctx.send("Нельзя так!")
                            return

                        c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                        do = int(c.fetchone()[0])
                        if sum == "all":
                            c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                            do = int(c.fetchone()[0])
                            c.execute(f"UPDATE users SET bank = 0 WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                            embed = disnake.Embed(title="**БАНК ПОСЛЕ СПИСАНИЯ**",
                                                description=f"<@!{usr.id}>, с вашего счета в банке были списаны все деньги! \n\nCумма до снятия: {do}<:hdollar:1038118641176162394>\nСумма после снятия: 0<:hdollar:1038118641176162394>",
                                                color=0xff0000,
                                                timestamp=ctx.message.created_at)
                            await ctx.send(embed=embed)

                        c.execute(f"UPDATE users SET bank = bank - {int(sum)} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")

                        c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                        posle = int(c.fetchone()[0])

                        embed = disnake.Embed(title="**БАНК ПОСЛЕ СПИСАНИЯ**",
                                            description=f"С счета {usr.mention}, было списано: {sum}<:hdollar:1038118641176162394>\n\nCумма до снятия: {do}<:hdollar:1038118641176162394>\nСумма после снятия: {posle}<:hdollar:1038118641176162394>",
                                            color=0xff0000,
                                            timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)
                        db.commit()

                    else:
                        await ctx.send("Неверная цель снятия")
                else:
                    await ctx.send("Это бот!")

    @commands.command(aliases=["переводб", "transferb"])
    @commands.guild_only()
    @pidor()
    async def __perevodb(self, ctx, usr: disnake.Member = None, sum=None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT serverid, channelid FROM bankomat WHERE serverid = {ctx.guild.id} AND channelid = {ctx.channel.id}")
                if c.fetchone() is None:
                    await ctx.send("В данном канале не установлен банкомат!<:onno:954815596082659368>")
                    return
                elif usr is None:
                    await ctx.send("Вы не указали цель перевода!")
                    return
                elif sum is None:
                    await ctx.send("Вы не указали сумму перевода!")
                    return
                else:
                    c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    if int(c.fetchone()[0]) < int(sum):
                        await ctx.send("На вашем счете недостаточно средств!")
                        return
                    else:
                        c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        dootp: str = c.fetchone()[0]
                        c.execute(f"UPDATE users SET bank = bank - {int(sum)} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        posotp: str = c.fetchone()[0]

                        c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                        dopol: str = c.fetchone()[0]

                        c.execute(f"UPDATE users SET bank = bank + {int(sum)} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                        pospol: str = c.fetchone()[0]

                        embed = disnake.Embed(title="**ПЕРЕВОД**",
                                            description=f"Участник {ctx.message.author.mention}, перевел на счет {usr.mention} {sum}<:hdollar:1038118641176162394>\n\nВаш счет до перевода: {dootp}<:hdollar:1038118641176162394>\nПосле: {posotp}<:hdollar:1038118641176162394>\n\nСчет получателя до перевода: {dopol}<:hdollar:1038118641176162394>\nПосле: {pospol}<:hdollar:1038118641176162394>",
                                            color=0x008000,
                                            timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)

    @commands.command(aliases=["положить", "dep"])
    @commands.guild_only()
    @pidor()
    async def __poloshit(self, ctx, suk = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT serverid, channelid FROM bankomat WHERE serverid = {ctx.guild.id} AND channelid = {ctx.channel.id}")
                if c.fetchone() is None:
                    await ctx.send("В данном канале не установлен банкомат!<:onno:954815596082659368>")
                    return
                if suk is None:
                    await ctx.send("Вы не указали сумму!")
                    return
                else:
                    ll = ["все", "всё", "all"]

                    if suk in ll:
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        if c.fetchone()[0] < 1:
                            await ctx.send("У вас нет денег!")
                            return
                        


                    c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    if int(c.fetchone()[0]) < int(suk):
                        await ctx.send("На вашем счете недостаточно средств!")
                    else:
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        baldo: str = c.fetchone()[0]
                        c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        bankdo: str = c.fetchone()[0]
                        c.execute(f"UPDATE users SET balance = balance - {int(suk)} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        balpos: str = c.fetchone()[0]
                        c.execute(f"UPDATE users SET bank = bank + {int(suk)} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        bankpos: str = c.fetchone()[0]
                        embed = disnake.Embed(title="**ПОПОЛНЕНИЕ**",
                                            description=f"{ctx.message.author.mention}, Вы пополнили свой счет на {int(suk)}<:hdollar:1038118641176162394>\n\nВаши наличные до операции: {baldo}\nПосле: {balpos}\n\nВаш счет в банке до операции: {bankdo}\nПосле: {bankpos}",
                                            color=0x008000,
                                            timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)

    @commands.command(aliases=["снять", "grab"])
    @commands.guild_only()
    @pidor()
    async def __snat(self, ctx, suk: int = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT serverid, channelid FROM bankomat WHERE serverid = {ctx.guild.id} AND channelid = {ctx.channel.id}")
                if c.fetchone() is None:
                    await ctx.send("В данном канале не установлен банкомат!<:onno:954815596082659368>")
                    return
                if suk is None:
                    await ctx.send("Вы не указали сумму!")
                    return
                else:
                    c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    if int(c.fetchone()[0]) < suk:
                        await ctx.send("На вашем счете недостаточно средств!<:onno:954815596082659368>")
                    else:
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        baldo: str = c.fetchone()[0]
                        c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        bankdo: str = c.fetchone()[0]
                        c.execute(f"UPDATE users SET balance = balance + {suk} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        balpos: str = c.fetchone()[0]
                        c.execute(f"UPDATE users SET bank = bank - {suk} WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        db.commit()
                        c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                        bankpos: str = c.fetchone()[0]
                        embed = disnake.Embed(title="**СНЯТИЕ**",
                                            description=f"{ctx.message.author.mention}, Вы сняли со своего банковского счета {suk}<:hdollar:1038118641176162394>\n\nВаши наличные до операции: {baldo}<:hdollar:1038118641176162394>\nПосле: {balpos}<:hdollar:1038118641176162394>\n\nВаш счет в банке до операции: {bankdo}<:hdollar:1038118641176162394>\nПосле: {bankpos}<:hdollar:1038118641176162394>",
                                            color=0x008000,
                                            timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)

    @commands.command(aliases=["add", "добавить"])
    @commands.guild_only()
    @pidor()
    @has_permissions(administrator=True)
    async def __add(self, ctx, usr: disnake.Member = None, sum=None, shet=None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if int(sum) < 1:
                    await ctx.send("Простите, но сумму меньше нуля, нельзя зачислить на счет!")
                    return

                if shet is None:
                    await ctx.send("Укажите в конце комманды счет. (банк или наличные)")
                elif shet.lower() == "наличные":
                    c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    do = c.fetchone()[0]
                    if int(do) >= 10000000000:
                        embed = disnake.Embed(title="**?**",
                                            description=f"{usr.mention}, вы меня конечно извините, но не слишком ли это?",
                                            color=0x00ff04,
                                            timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)
                        return
                    c.execute(f"UPDATE users SET balance = balance + {int(sum)} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    db.commit()
                    embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{usr.mention}, на ваш карман было зачислено {sum}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)
                elif shet.lower() == "банк":
                    c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    do = c.fetchone()[0]
                    if int(do) >= 10000000000:
                        embed = disnake.Embed(title="**?**",
                                            description=f"{usr.mention}, вы меня конечно извините, но не слишком ли это?",
                                            color=0x008000,
                                            timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)
                        return
                    c.execute(f"UPDATE users SET bank = bank + {int(sum)} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    db.commit()
                    embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{usr.mention}, на ваш банк было зачислено {sum}<:hdollar:1038118641176162394>\n\nВаша сумма в банке до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x00ff04,
                                        timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Неверная цель")

    @commands.command(aliases=["баланс", "balance"])
    @commands.guild_only()
    @pidor()
    async def __balance(self, ctx, usr: disnake.Member = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if usr is None:
                    c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    nalis = c.fetchone()[0]
                    c.execute(f"SELECT bank FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")
                    bank = c.fetchone()[0]
                    embed = disnake.Embed(title="**БАЛАНС**",
                                        description=f"<@!{ctx.message.author.id}>\n\nВаши наличные: {nalis}<:hdollar:1038118641176162394>\nВ банке: {bank}<:hdollar:1038118641176162394>",
                                        color=0x00ff04,
                                        timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)

                else:
                    c.execute(f"SELECT balance FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    nalis = c.fetchone()[0]
                    c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                    bank = c.fetchone()[0]
                    embed = disnake.Embed(title="**БАЛАНС**",
                                        description=f"<@!{ctx.message.author.id}>\n\nНаличных у {usr.mention}: {nalis}<:hdollar:1038118641176162394>\nВ банке: {bank}",
                                        color=0x00ff04,
                                        timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)

    @commands.command(aliases=["leaderboard", "лидеры"])
    @commands.guild_only()
    @pidor()
    async def __leaderboard(self, ctx):
        embed = disnake.Embed(title="**ТОП 10 СЕРВЕРА**", color=0x7000cc, timestamp=ctx.message.created_at)

        counter = 0
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT userid FROM users WHERE serverid = {ctx.guild.id} ORDER BY bank DESC LIMIT 10")
                a = c.fetchall()

                for n in a:
                    counter += 1
                    usr = self.bot.get_user(n[0])
                    embed.add_field(
                        name=f"** **",
                        value=f"{counter}# | {usr.mention}",
                        inline=False)
                    c.execute(f"SELECT bank FROM users WHERE serverid = {ctx.guild.id} AND userid = {n[0]}")
                    embed.add_field(
                        name=f"Банк: {c.fetchone()[0]}<:hdollar:1038118641176162394>;\n\n",
                        value=f"** **",
                        inline=False)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(eko(bot))
