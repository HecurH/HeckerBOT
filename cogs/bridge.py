import asyncio
from contextlib import closing
import os
import random
import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions, bot_has_permissions
import psycopg2
from config import password, host, db_name, bid

from config import user as userr

import datetime
from disnake.enums import ButtonStyle
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


def rem_money(bott, id: int, money: int, bank: bool, ctx):
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
                c.execute(f"UPDATE users SET balance = balance - {money} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                db.commit()
                return True
            if bank is True:
                usr = bott.get_user(id)
                c.execute(f"SELECT bank FROM users WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                bank = c.fetchone()
                if bank is None:
                    return False
                c.execute(f"UPDATE users SET bank = bank - {money} WHERE userid = {usr.id} AND serverid = {ctx.guild.id}")
                db.commit()
                return True



class one(disnake.ui.View):
    msg: disnake.Message
    
    def __init__(self, counter: int, id: int, ctx, bot, stavka):
        super().__init__(timeout=100)
        self.counter = counter
        self.ctx = ctx
        self.bot = bot
        self.stavka = stavka


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

    @disnake.ui.button(label="1", style=ButtonStyle.grey)
    async def first_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if self.counter >= 8:
                    await inter.response.send_message("Афигеть, ты выиграл! Твоя ставка увеличена в 10 раз.")
                    c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                    do = c.fetchone()[0]
                    add_money(self.bot, self.ctx.author.id, int(self.stavka)*10, False, self.ctx)
                    c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                    embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {int(self.stavka)*10}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                    await inter.followup.send(embed=embed)
                    self.children[0].disabled = True  # type: ignore
                    self.children[1].disabled = True  # type: ignore
                    try:
                        await self.msg.edit(view=self)
                    except:
                        pass
                    self.stop()
                    return



                o = random.randint(1, 2)
                if o == 1:
                    oo = random.randint(1, 100)
                    if oo == 1:
                        embed = disnake.Embed(title="**О ГОСПОДИ**",
                                        description=f"Вас посетила священная капибара! Она отговорила вас от этой кнопки. (переход на следующий этап)",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        embed.set_image('https://cs14.pikabu.ru/post_img/2022/03/11/6/1646990230224889342.jpg')
                        await inter.response.send_message(embed=embed)
                        self.counter += 1
                        for child in self.children:
                            if isinstance(child, disnake.ui.Button):
                                child.disabled = True

                        await inter.followup.edit_message(message_id=self.msg.id,view=self)
                        self.stop()
                        view = one(self.counter, self.ctx.message.id, self.ctx, self.bot, self.stavka)
                        

                        view.msg = await inter.followup.send("Повезло вдвойне!", view=view, file=disnake.File('111.png'))
                        return
                    if self.counter == 1:
                        await inter.response.send_message("Вы проиграли! И не получите **ничего**, ибо вы на первой стадии.")
                        rem_money(self.bot, self.ctx.author.id, self.stavka, False, self.ctx)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 2:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 1.5 раза! (капитал будет округлен)")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, round(self.stavka*1.5), False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {round(self.stavka*1.5)}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)             
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()   
                        return
                    if self.counter == 3:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 2 раза!")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, self.stavka*2, False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {self.stavka*2}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 4:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 2.5 раза! (капитал будет округлен)")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, round(self.stavka*2.5), False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {round(self.stavka*2.5)}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 5:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 4 раза!")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, self.stavka*4, False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {self.stavka*4}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 6:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 6 раз!")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, self.stavka*6, False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {self.stavka*6}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 7:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 7 раза!")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, self.stavka*7, False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {self.stavka*7}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                elif o == 2:
                    self.counter += 1
                    view = one(self.counter, self.ctx.message.id, self.ctx, self.bot, self.stavka)
                    self.children[0].disabled = True  # type: ignore
                    self.children[1].disabled = True  # type: ignore
                    try:
                        await self.msg.edit(view=self)
                    except:
                        pass
                    self.stop()

                    view.msg = await inter.response.send_message("Повезло!", view=view, file=disnake.File('111.png'))
    @disnake.ui.button(label="2", style=ButtonStyle.grey)
    async def not_first_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if self.counter >= 8:
                    await inter.response.send_message("Афигеть, ты выиграл! Твоя ставка увеличена в 10 раз.")
                    c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                    do = c.fetchone()[0]
                    add_money(self.bot, self.ctx.author.id, int(self.stavka)*10, False, self.ctx)
                    c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                    embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {int(self.stavka)*10}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                    await inter.followup.send(embed=embed)
                    self.children[0].disabled = True  # type: ignore
                    self.children[1].disabled = True  # type: ignore
                    try:
                        await self.msg.edit(view=self)
                    except:
                        pass
                    self.stop()
                    return



                o = random.randint(1, 2)
                if o == 1:
                    oo = random.randint(1, 100)
                    if oo == 1:
                        embed = disnake.Embed(title="**О ГОСПОДИ**",
                                        description=f"Вас посетила священная капибара! Она отговорила вас от этой кнопки. (переход на следующий этап)",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        embed.set_image('https://cs14.pikabu.ru/post_img/2022/03/11/6/1646990230224889342.jpg')
                        await inter.response.send_message(embed=embed)
                        self.counter += 1
                        for child in self.children:
                            if isinstance(child, disnake.ui.Button):
                                child.disabled = True

                        await inter.followup.edit_message(message_id=self.msg.id,view=self)
                        self.stop()
                        view = one(self.counter, self.ctx.message.id, self.ctx, self.bot, self.stavka)
                        

                        view.msg = await inter.followup.send("Повезло вдвойне!", view=view, file=disnake.File('111.png'))
                        return

                    if self.counter == 1:
                        await inter.response.send_message("Вы проиграли! И не получите **ничего**, ибо вы на первой стадии.")
                        rem_money(self.bot, self.ctx.author.id, self.stavka, False, self.ctx)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 2:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 1.5 раза! (капитал будет округлен)")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, round(self.stavka*1.5), False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {round(self.stavka*1.5)}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)             
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()   
                        return
                    if self.counter == 3:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 2 раза!")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, self.stavka*2, False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {self.stavka*2}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 4:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 2.5 раза! (капитал будет округлен)")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, round(self.stavka*2.5), False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {round(self.stavka*2.5)}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 5:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 4 раза!")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, self.stavka*4, False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {self.stavka*4}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 6:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 6 раз!")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, self.stavka*6, False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {self.stavka*6}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                    if self.counter == 7:
                        await inter.response.send_message("Вы проиграли! Вы приумножили свой капитал в 7 раза!")
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        do = c.fetchone()[0]
                        add_money(self.bot, self.ctx.author.id, self.stavka*7, False, self.ctx)
                        c.execute(f"SELECT balance FROM users WHERE userid = {self.ctx.author.id} AND serverid = {self.ctx.guild.id}")
                        embed = disnake.Embed(title="**БАЛАНС ПОСЛЕ ЗАЧИСЛЕНИЯ**",
                                        description=f"{self.ctx.author.mention}, на ваш карман было зачислено {self.stavka*7}<:hdollar:1038118641176162394>\n\nВаша сумма до пополнения: {do}<:hdollar:1038118641176162394>\nПосле: {c.fetchone()[0]}<:hdollar:1038118641176162394>",
                                        color=0x008000,
                                        timestamp=self.ctx.message.created_at)
                        await inter.followup.send(embed=embed)
                        self.children[0].disabled = True  # type: ignore
                        self.children[1].disabled = True  # type: ignore
                        try:
                            await self.msg.edit(view=self)
                        except:
                            pass
                        self.stop()
                        return
                elif o == 2:
                    self.counter += 1
                    for child in self.children:
                        if isinstance(child, disnake.ui.Button):
                            child.disabled = True

                    await inter.response.edit_message(view=self)
                    self.stop()
                    view = one(self.counter, self.ctx.message.id, self.ctx, self.bot, self.stavka)
                    
                    view.msg = await inter.followup.send("Повезло!", view=view, file=disnake.File('111.png'))



    


    
class bridge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases = ["bridge", "мост"])
    @commands.guild_only()
    @pidor()
    async def __briddge(self, ctx, stavka: int = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                if stavka is None:
                    await ctx.send("Ты ставку не указал!")
                    return
                elif stavka < 10:
                    await ctx.send("Минимальная ставка 10<:hdollar:1038118641176162394>!")
                    return
                c.execute(f"SELECT balance FROM users WHERE userid = {ctx.message.author.id} AND serverid = {ctx.guild.id}")    
                if stavka > c.fetchone()[0]:
                    await ctx.send("У вас недостаточно средств!")
                    return

                yep = ["y", "yes", "д", "да"]
                embed = disnake.Embed(title="**СТЕКЛЯННЫЙ МОСТ**", description="Каждый раз, я буду давать вам две кнопки, но только одна из них будет верна. Чем больше кнопок сумеете нажать - тем больше выиграете", color=0x7000cc)

                await ctx.send(embed=embed)
                await ctx.send("Если вы согласны с условиями игры и своей ставкой, напишите 'Да', иначе - 'Нет'")
                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author

                message1 = await self.bot.wait_for('message', check=check, timeout=60)
                if message1.content.lower() in yep:


                    view = one(1, ctx.message.id, ctx, self.bot, stavka)
                
                
                    view.msg = await ctx.send("Ну, удачи.", view=view, file=disnake.File('111.png'))
                else:
                    await ctx.send("Игра отменена!")




def setup(bot):
    bot.add_cog(bridge(bot))

