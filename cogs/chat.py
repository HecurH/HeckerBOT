import asyncio
from contextlib import closing
import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions, bot_has_permissions
import psycopg2
from config import password, host, db_name, bid
import datetime
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



class chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['подарить', 'gift'])
    @bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @pidor()
    async def __gift(self, ctx, usr: int, inp = None, sett: int = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {ctx.message.guild.id} AND enabled = 'Enabled'")
                if c.fetchone() is None:
                    await ctx.send("У вашего сервера не включен чат или не установлен канал!")
                    return
                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {ctx.message.guild.id} AND gifton = 'Enabled'")
                if c.fetchone() is None:
                    await ctx.send("У вашего сервера не включен обмен!")
                    return
                c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id} AND gifton = 'Enabled'")
                if c.fetchone() is None:
                    await ctx.send("У вашего сервера нет сопряженного сервера!")
                    return

                if usr is None:
                    await ctx.send("Вы не указали айди для обмена!")
                    return
                if inp is None:
                    await ctx.send("Вы не указали предмет для обмена!")
                    return
                if sett is None:
                    await ctx.send("Вы не указали кол-во предметов для обмена!")
                    return
                c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id} AND gifton = 'Enabled'")
                guildtu = self.bot.get_guild(c.fetchone()[0])
                user = self.bot.get_user(usr)
                if user is None:
                    await ctx.send("Не могу найти данного пользователя!")
                    return
                if user not in guildtu.members:
                    await ctx.send("Не могу найти данного пользователя в сопряженном сервере!")
                    return
                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {guildtu.id} AND gifton = 'Enabled'")
                if c.fetchone() is None:
                    await ctx.send("У этого сервера не включен обмен!")
                    return

                if inp == "арбуз":
                    if sett < 1:
                        await ctx.send("Ты тютю?")
                        return
                    c.execute(f"SELECT waterm FROM users WHERE serverid = {guildtu.id} AND userid = {user.id}")
                    do_waterm_pol = c.fetchone()[0]

                    c.execute(f"SELECT waterm FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    do_waterm = c.fetchone()[0]
                    if do_waterm == 0:
                        await ctx.send("У вас нет арбузов для обмена!")
                        return
                    if do_waterm < sett:
                        await ctx.send("У вас нет столько арбузов для обмена!")
                        return
                    c.execute(f"UPDATE users SET waterm = waterm - {sett} WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    c.execute(f"UPDATE users SET waterm = waterm + {sett} WHERE serverid = {guildtu.id} AND userid = {user.id}")
                    db.commit()
                    c.execute(f"SELECT waterm FROM users WHERE serverid = {guildtu.id} AND userid = {user.id}")
                    pos_waterm_pol = c.fetchone()[0]

                    c.execute(f"SELECT waterm FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    pos_waterm = c.fetchone()[0]
                    embed = disnake.Embed(title="**УСПЕХ**",
                                                description=f"<@!{ctx.message.author.id}>, \n\nОтправлено!\nВаш арбузы до: {do_waterm}\nПосле: {pos_waterm}\n\nЕго арбузы до: {do_waterm_pol}\nПосле: {pos_waterm_pol}",
                                                color=0x7000cc)
                    await ctx.send(embed=embed)
                    await user.send(f"Вам отправили арбуз/ы ({sett})")
                elif inp == "бутерброд":
                    if sett < 1:
                        await ctx.send("Ты тютю?")
                        return
                    c.execute(f"SELECT sandw FROM users WHERE serverid = {guildtu.id} AND userid = {user.id}")
                    do_waterm_pol = c.fetchone()[0]

                    c.execute(f"SELECT sandw FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    do_waterm = c.fetchone()[0]
                    if do_waterm == 0:
                        await ctx.send("У вас нет бутербродов для обмена!")
                        return
                    if do_waterm < sett:
                        await ctx.send("У вас нет столько бутербродов для обмена!")
                        return
                    c.execute(f"UPDATE users SET sandw = sandw - {sett} WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    c.execute(f"UPDATE users SET sandw = sandw + {sett} WHERE serverid = {guildtu.id} AND userid = {user.id}")
                    db.commit()
                    c.execute(f"SELECT sandw FROM users WHERE serverid = {guildtu.id} AND userid = {user.id}")
                    pos_waterm_pol = c.fetchone()[0]

                    c.execute(f"SELECT sandw FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    pos_waterm = c.fetchone()[0]
                    embed = disnake.Embed(title="**УСПЕХ**",
                                                description=f"<@!{ctx.message.author.id}>, \n\nОтправлено!\nВаш бутерброды до: {do_waterm}\nПосле: {pos_waterm}\n\nЕго бутерброды до: {do_waterm_pol}\nПосле: {pos_waterm_pol}",
                                                color=0x7000cc)
                    await ctx.send(embed=embed)
                    await user.send(f"Вам отправили бутерброд/ы ({sett})")
                else:
                    await ctx.send("Неверное условие!")





    @commands.command(aliases=['обмен', 'swap'])
    @bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @pidor()
    async def __swap(self, ctx, inp = None, sett: int = None):
        if inp is None:
            await ctx.send("Вы не указали что хотите обменять! (бутерброд/арбуз)")
            return
        elif inp == "бутерброд":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    if sett is None:
                        await ctx.send("Вы не указали кол-во!")
                        return
                    if sett < 1:
                        await ctx.send("Ты тютю?")
                        return
                    c.execute(f"SELECT sandw FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    sandw = c.fetchone()
                    if sandw[0] == 0:
                        await ctx.send("У вас нет бутербродов для обмена")
                        return
                    if sandw[0] < sett:
                        await ctx.send("У вас нет столько бутербродов для обмена!")
                        return

                    c.execute(f"SELECT sandwc FROM guild WHERE serverid = {ctx.message.guild.id}")
                    cost: int = c.fetchone()[0]


                    do_sandw = sandw[0]
                    c.execute(f"SELECT balance FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    do_bal = c.fetchone()[0]
                    c.execute(f"UPDATE users SET balance = balance + {sett*cost} WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    c.execute(f"UPDATE users SET sandw = sandw - {sett} WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    db.commit()

                    c.execute(f"SELECT sandw FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    pos_sandw = c.fetchone()[0]
                    c.execute(f"SELECT balance FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    pos_bal = c.fetchone()[0]
                    embed = disnake.Embed(title="**УСПЕХ**",
                                                description=f"<@!{ctx.message.author.id}>, \n\nПреобразование успешно!\nВаш наличные до преобразования: {do_bal}<:hdollar:1038118641176162394>\nВаш наличные после: {pos_bal}<:hdollar:1038118641176162394>\n\nВаши бутерброды до: {do_sandw}\nПосле: {pos_sandw}",
                                                color=0x7000cc)
                    await ctx.send(embed=embed)
        elif inp == "арбуз":
            if sett is None:
                await ctx.send("Вы не указали кол-во!")
                return
            if sett < 1:
                await ctx.send("Ты тютю?")
                return
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT waterm FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    waterm = c.fetchone()
                    if waterm[0] == 0:
                        await ctx.send("У вас нет арбузов для обмена")
                        return
                    if waterm[0] < sett:
                        await ctx.send("У вас нет столько арбузов для обмена!")
                        return

                    c.execute(f"SELECT watermc FROM guild WHERE serverid = {ctx.message.guild.id}")
                    cost: int = c.fetchone()[0]


                    do_waterm = waterm[0]
                    c.execute(f"SELECT balance FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    do_bal = c.fetchone()[0]
                    c.execute(f"UPDATE users SET balance = balance + {sett*cost} WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    c.execute(f"UPDATE users SET waterm = waterm - {sett} WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    db.commit()

                    c.execute(f"SELECT waterm FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    pos_waterm = c.fetchone()[0]
                    c.execute(f"SELECT balance FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    pos_bal = c.fetchone()[0]
                    embed = disnake.Embed(title="**УСПЕХ**",
                                                description=f"<@!{ctx.message.author.id}>, \n\nПреобразование успешно!\nВаш наличные до преобразования: {do_bal}<:hdollar:1038118641176162394>\nВаш наличные после: {pos_bal}<:hdollar:1038118641176162394>\n\nВаши арбузы до: {do_waterm}\nПосле: {pos_waterm}",
                                                color=0x7000cc)
                    await ctx.send(embed=embed)
        else:
            await ctx.send("Неверное условие!")




    @commands.command(aliases=['уровень_а', 'lvl_a'])
    @has_permissions(administrator=True)
    @bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @pidor()
    async def __llfdsdfflvl(self, ctx, inp = None, sett: int = None):
        if inp is None:
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    embed = disnake.Embed(title="**НАСТРОЙКИ УРОВНЕЙ**", color=0x7000cc, timestamp=ctx.message.created_at)
                    c.execute(f"SELECT sandwc FROM guild WHERE serverid = {ctx.message.guild.id}")
                    maxwarnss = c.fetchone()[0]
                    embed.add_field(
                                name=f"Цена бутербродов (по умолчанию - 2800<:hdollar:1038118641176162394>)",
                                value=maxwarnss,
                                inline=True
                            )

                    c.execute(f"SELECT watermc FROM guild WHERE serverid = {ctx.message.guild.id}")
                    warnschannel = c.fetchone()[0]


                    embed.add_field(
                                name=f"Цена арбузов (по умолчанию - 9000<:hdollar:1038118641176162394>)",
                                value=warnschannel,
                                inline=True
                            )

                    c.execute(f"SELECT gifton FROM guild WHERE serverid = {ctx.message.guild.id}")
                    gifton = c.fetchone()[0]
                    embed.add_field(
                                name=f"Включены ли подарки",
                                value=gifton,
                                inline=True
                            )

                    await ctx.send(embed=embed)
        elif inp == "бутерброд":
            if sett is None:
                await ctx.send("Вы не указали цену!")
                return

            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"UPDATE guild SET sandwc = {sett} WHERE serverid = {ctx.message.guild.id}")
                    db.commit()
            await ctx.send("Цена изменена!")

        elif inp == "арбуз":
            if sett is None:
                await ctx.send("Вы не указали цену!")
                return
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"UPDATE guild SET watermc = {sett} WHERE serverid = {ctx.message.guild.id}")
                    db.commit()
            await ctx.send("Цена изменена!")
        elif inp == "подарки":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT gifton FROM guild WHERE serverid = {ctx.message.guild.id}")
                    a = c.fetchone()[0]
                    if a == "Disabled":
                        c.execute(f"UPDATE guild SET gifton = 'Enabled' WHERE serverid = {ctx.message.guild.id}")
                        db.commit()

                        embed = disnake.Embed(title="**УСПЕШНО**",
                                description=f'Межсерверный обмен включен.',
                                color=0x5900ff,
                                timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)

                    elif a == "Enabled":
                        c.execute(f"UPDATE guild SET gifton = 'Disabled' WHERE serverid = {ctx.message.guild.id}")
                        db.commit()

                        embed = disnake.Embed(title="**УСПЕШНО**",
                                description=f'Межсерверный обмен выключен.',
                                color=0x5900ff,
                                timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)
            


    @commands.command(aliases=['lvl', 'уровень'])
    @commands.guild_only()
    @pidor()
    async def __lvl(self, ctx, usr: disnake.Member = None):
        if usr is None:
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT chnlid FROM guild WHERE serverid = {ctx.message.guild.id} AND enabled = 'Enabled'")
                    if c.fetchone() is None:
                        await ctx.send("У вашего сервера не включен чат или не установлен канал!")
                        return
                    c.execute(f"SELECT counter FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    count = c.fetchone()[0]
                    c.execute(f"SELECT lvl FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    lvl = c.fetchone()[0]
                    c.execute(f"SELECT sandw FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    sandw = c.fetchone()[0]
                    c.execute(f"SELECT waterm FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {ctx.message.author.id}")
                    waterm = c.fetchone()[0]

                    if lvl == 0:
                        maxcount = 50
                    else:
                        maxcount = 50*lvl
                    embed = disnake.Embed(title="**ИНФОРМАЦИЯ**", description=f"Опыт: {count}/{maxcount}\nУровень: {lvl}\nБутерброды: {sandw}\nАрбузы: {waterm}", color=0x7000cc, timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)
        else:
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT chnlid FROM guild WHERE serverid = {ctx.message.guild.id} AND enabled = 'Enabled'")
                    if c.fetchone() is None:
                        await ctx.send("У вашего сервера не включен чат или не установлен канал!")
                        return
                    c.execute(f"SELECT counter FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {usr.id}")
                    count = c.fetchone()[0]
                    c.execute(f"SELECT lvl FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {usr.id}")
                    lvl = c.fetchone()[0]
                    c.execute(f"SELECT sandw FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {usr.id}")
                    sandw = c.fetchone()[0]
                    c.execute(f"SELECT waterm FROM users WHERE serverid = {ctx.message.guild.id} AND userid = {usr.id}")
                    waterm = c.fetchone()[0]

                    if lvl != 0:
                        maxcount = maxcount * lvl
                    embed = disnake.Embed(title="**ИНФОРМАЦИЯ ОБ ЭТОМ ПОЛЬЗОВАТЕЛЕ**", description=f"Опыт: {count}/{maxcount}\nУровень: {lvl}\nБутерброды: {sandw}\nАрбузы: {waterm}", color=0x7000cc, timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)

    @commands.command(aliases=['rollback'])
    @pidor()
    async def __llfadffwordd(self, ctx):
        if ctx.message.author.id not in bid:
            return
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute("ROLLBACK")
                db.commit()


    @commands.command(aliases=['чат_серв', 'chat_serv'])
    @has_permissions(administrator=True)
    @bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @pidor()
    async def __llfadffword(self, ctx, inp = None, sett: int = None):
        if inp is None:
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    embed = disnake.Embed(title="**ДОСТУПНЫЕ СЕРВЕРА**", color=0x7000cc, timestamp=ctx.message.created_at)
                    c.execute(f"SELECT serverid FROM guild WHERE serverid = {ctx.guild.id} AND enabled = 'Enabled' AND serveridtu = 0")

                    if c.fetchone() is None:
                        await ctx.send("Нет доступных серверов! (Или вы уже сопряжены)")
                        return
                    else:
                        c.execute(f"SELECT serverid FROM guild WHERE enabled = 'Enabled' AND serveridtu = 0")
                        for n in c.fetchall():
                            a = self.bot.get_guild(n[0])
                            if a.id is not ctx.message.guild.id:

                                embed.add_field(
                                    name=f"** **",
                                    value=f"{a.name} - {a.id}, ",
                                    inline=False
                                )
                                embed.add_field(
                                    name=f"Участники: {len(a.members)};\n\n",
                                    value=f"** **",
                                    inline=False
                                )
                        await ctx.send(embed=embed)

        elif inp == "добавить":
            if sett is None:
                await ctx.send("Вы не указали айди сервера для спряжения!")
                return
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id}")
                    if c.fetchone()[0] == 0:
                        c.execute(f"SELECT serverid FROM guild WHERE serverid = {sett} AND enabled = 'Enabled' AND serveridtu = 0")
                        if c.fetchone() is not None:
                            c.execute(f"SELECT chnlid FROM guild WHERE serverid = {sett} AND enabled = 'Enabled' AND serveridtu = 0")
                            if c.fetchone() is None:
                                await ctx.send("У этого сервера не установлен чат!")
                                return
                            else:
                                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {ctx.message.guild.id} AND enabled = 'Enabled' AND serveridtu = 0")
                                if c.fetchone() is None:
                                    await ctx.send("У вашего сервера не включен чат или не установлен канал!")
                                    return
                                else:
                                    c.execute(f"SELECT chnlid FROM guild WHERE serverid = {sett} AND enabled = 'Enabled' AND serveridtu = 0")
                                    ada = c.fetchone()[0]
                                    c.execute(f"SELECT chnlid FROM guild WHERE serverid = {ctx.message.guild.id} AND enabled = 'Enabled' AND serveridtu = 0")
                                    ava = c.fetchone()[0]
                                    a = self.bot.get_channel(ada)
                                    b = self.bot.get_channel(ava)
                                    cc = self.bot.get_guild(sett)
                                    if a not in cc.channels:
                                        await ctx.send("У этого сервера проблема с каналом!")
                                        await cc.owner.send("Здравствуйте! Бот столкнулся с проблемой, он не видит канала для межсерверного чата (к вам попытались присоединиться)")
                                        c.execute("UPDATE guild SET chnlid = %s WHERE serverid = %s AND enabled = %s AND serveridtu = %s", (None, sett, 'Enabled', 0))
                                        db.commit()
                                        return
                                    if b not in ctx.message.guild.channels:
                                        await ctx.send("У вашего сервера проблема с каналом!")
                                        c.execute("UPDATE guild SET chnlid = %s WHERE serverid = %s AND enabled = %s AND serveridtu = %s", (None, ctx.message.guild.id, 'Enabled', 0))
                                        db.commit()
                                        return
                                    c.execute(f"SELECT serverid FROM bannedg WHERE serveridown = {sett} AND serverid = {ctx.message.guild.id}")
                                    if c.fetchone() is not None:
                                        c.execute(f"SELECT reason FROM bannedg WHERE serveridown = {sett} AND serverid = {ctx.message.guild.id}")
                                        await ctx.send(f"Этот сервер вас забанил! Причина: {c.fetchone()[0]}")
                                        return
                                    c.execute(f"SELECT serverid FROM bannedg WHERE serveridown = {ctx.message.guild.id} AND serverid = {sett}")
                                    if c.fetchone() is not None:
                                        c.execute(f"SELECT reason FROM bannedg WHERE serveridown = {ctx.message.guild.id} AND serverid = {sett}")
                                        await ctx.send(f"Вы забанили этот сервер! Причина: {c.fetchone()[0]}")
                                        return
                                    c.execute(f"UPDATE guild SET serveridtu = {sett} WHERE serverid = {ctx.message.guild.id}")
                                    c.execute(f"UPDATE guild SET serveridtu = {ctx.message.guild.id} WHERE serverid = {sett}")
                                    db.commit()
                                    await ctx.send("Спряжение удачно!")
                                    await a.send(f"С вами был соединен сервер '{ctx.message.guild.name}'")
                        else:
                            await ctx.send("У этого сервера не включен чат или уже есть сопряженный сервер!")
                    else:
                        await ctx.send("У этого сервера уже есть сопряженный сервер!")
        elif inp == "удалить":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id}")
                    if c.fetchone() == 0:
                        await ctx.send("У вас нет сопряженного сервера для удаления!")
                        return
                    c.execute(f"SELECT chnlid FROM guild WHERE serveridtu = {ctx.message.guild.id}")
                    a = c.fetchone()

                    c.execute(f"SELECT serverid FROM banned WHERE serverid = {ctx.guild.id}")
                    if c.fetchone() is not None:
                        c.execute(f"DELETE FROM banned WHERE serverid = {ctx.guild.id}")


                    c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id}")
                    c.execute(f"SELECT serverid FROM banned WHERE serverid = {c.fetchone()[0]}")
                    if c.fetchone() is not None:
                        c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id}")
                        c.execute(f"DELETE FROM banned WHERE serverid = {c.fetchone()[0]}")
                    c.execute(f"UPDATE guild SET serveridtu = 0 WHERE serverid = {ctx.message.guild.id}")
                    c.execute(f"UPDATE guild SET serveridtu = 0 WHERE serveridtu = {ctx.message.guild.id}")
                    db.commit()
                    
                    await ctx.send("Успешно!")
                    
                    if a is None:
                        return
                    a = self.bot.get_channel(a[0])
                    await a.send("Сервер отсоединен.")
        elif inp == "бан":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id}")
                    if c.fetchone()[0] == 0:
                        await ctx.send("У вас нет сопряженного сервера!")
                        return
                    guild = ctx.message.guild
                    c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {guild.id}")
                    guildtu = self.bot.get_guild(c.fetchone()[0])
                    if sett is None:
                        await ctx.send("Вы не указали айди для бана!")
                        return
                    usr = self.bot.get_user(sett)
                    c.execute(f"SELECT memberid FROM banned WHERE serverid = {ctx.message.guild.id} AND memberid = {sett}")
                    if c.fetchone() is not None:
                        await ctx.send("Этот пользователь уже забанен!")
                        return


                    if usr in guildtu.members:
                        c.execute(f"INSERT INTO banned (serverid, reason, memberid) VALUES (%s, %s, %s)", (ctx.message.guild.id, 'Причину нельзя указать', sett))
                        db.commit()
                        await ctx.send("Успешно!")
                        await usr.send("Вас забанили для межсерверного чата!")
        elif inp == "разбан":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id}")
                    if c.fetchone()[0] == 0:
                        await ctx.send("У вас нет сопряженного сервера!")
                        return
                    guild = ctx.message.guild
                    c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {guild.id}")
                    guildtu = self.bot.get_guild(c.fetchone()[0])
                    if sett is None:
                        await ctx.send("Вы не указали айди для бана!")
                        return
                    usr = self.bot.get_user(sett)
                    c.execute(f"SELECT memberid FROM banned WHERE serverid = {ctx.message.guild.id} AND memberid = {sett}")
                    if c.fetchone() is None:
                        await ctx.send("Этот пользователь не забанен!")
                        return


                    if usr in guildtu.members:
                        c.execute(f"DELETE FROM banned WHERE serverid = {ctx.message.guild.id} AND memberid = {sett}")
                        db.commit()
                        await ctx.send("Успешно!")
                        await usr.send("Вас разбанили для межсерверного чата!")
        elif inp == "банлист":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    embed = disnake.Embed(title="**БАНЛИСТ**", color=0x7000cc, timestamp=ctx.message.created_at)
                    c.execute(f"SELECT serverid FROM banned WHERE serverid = {ctx.guild.id}")

                    if c.fetchone() is None:
                        await ctx.send("У вас нет забаненных!")
                        return
                    else:
                        c.execute(f"SELECT memberid FROM banned WHERE serverid = {ctx.guild.id}")
                        for n in c.fetchall():
                            embed.add_field(
                                name=f"** **",
                                value=f"{self.bot.get_user(n[0]).mention} - {self.bot.get_user(n[0]).id}, ",
                                inline=False
                            )

                        await ctx.send(embed=embed)






            



        elif inp == "бан-с":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    guild = ctx.message.guild
                    if sett is None:
                        await ctx.send("Вы не указали айди для бана!")
                        return
                    guban = self.bot.get_guild(sett)
                    c.execute(f"SELECT serverid FROM bannedg WHERE serveridown = {ctx.message.guild.id} AND serverid = {sett}")
                    if c.fetchone() is not None:
                        await ctx.send("Этот сервер уже забанен!")
                        return



                    c.execute(f"INSERT INTO bannedg (serverid, reason, serveridown) VALUES (%s, %s, %s)", (sett, 'Причину нельзя указать', ctx.message.guild.id))
                    db.commit()
                    await ctx.send("Успешно!")
        elif inp == "разбан-с":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    guild = ctx.message.guild
                    
                    if sett is None:
                        await ctx.send("Вы не указали айди для разбана!")
                        return
                    c.execute(f"SELECT serverid FROM bannedg WHERE serveridown = {guild.id} AND serverid = {sett}")
                    a = c.fetchone()
                    if a is None:
                        await ctx.send("Этот сервер не забанен!")
                        return
                    guildtu = self.bot.get_guild(a[0])

                    c.execute(f"DELETE FROM bannedg WHERE serveridown = {ctx.message.guild.id} AND serverid = {sett}")
                    db.commit()
                    await ctx.send("Успешно!")
        elif inp == "банлист-с":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    embed = disnake.Embed(title="**БАНЛИСТ-C**", color=0x7000cc, timestamp=ctx.message.created_at)
                    c.execute(f"SELECT serverid FROM bannedg WHERE serveridown = {ctx.guild.id}")

                    if c.fetchone() is None:
                        await ctx.send("У вас нет забаненных!")
                        return
                    else:
                        c.execute(f"SELECT serverid FROM bannedg WHERE serveridown = {ctx.guild.id}")
                        for n in c.fetchall():
                            embed.add_field(
                                name=f"** **",
                                value=f"{self.bot.get_guild(n[0]).name} - {self.bot.get_guild(n[0]).id}, ",
                                inline=False
                            )

                        await ctx.send(embed=embed)
        else:
            await ctx.send("Неверный аргумент!")
















    @commands.command(aliases=['чат_а', 'chat_a'])
    @has_permissions(administrator=True)
    @bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @pidor()
    async def __llfdsdffword(self, ctx, inp = None, sett: disnake.TextChannel = None):
        if inp is None:
            await ctx.send("Вы не указали аргумент!")
            return

        ll = ['переключить', 'канал']
        if inp not in ll:
            await ctx.send("Неверный аргумент! Пример этой команды - *чат_а переключить, или чат_а канал <упоминание канала>")
            return
        if inp == "переключить":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT enabled FROM guild WHERE serverid = {ctx.message.guild.id}")
                    a = c.fetchone()[0]
                    if a == "Disabled":
                        c.execute(f"UPDATE guild SET enabled = 'Enabled' WHERE serverid = {ctx.message.guild.id}")
                        db.commit()
                        c.execute(f"SELECT chnlid FROM guild WHERE serverid = {ctx.message.guild.id}")
                        b = c.fetchone()[0]
                        if b is None:
                            embed = disnake.Embed(title="**УСПЕШНО**",
                                    description=f'Межсерверный чат включен, НО у вас не указан канал для него. (пример - *чат_а канал <упоминание канала>)',
                                    color=0x5900ff,
                                    timestamp=ctx.message.created_at)
                            await ctx.send(embed=embed)
                        else:
                            embed = disnake.Embed(title="**УСПЕШНО**",
                                    description=f'Межсерверный чат включен.',
                                    color=0x5900ff,
                                    timestamp=ctx.message.created_at)
                            await ctx.send(embed=embed)
                    elif a == "Enabled":
                        c.execute(f"UPDATE guild SET enabled = 'Disabled' WHERE serverid = {ctx.message.guild.id}")
                        db.commit()

                        embed = disnake.Embed(title="**УСПЕШНО**",
                                description=f'Межсерверный чат выключен.',
                                color=0x5900ff,
                                timestamp=ctx.message.created_at)
                        await ctx.send(embed=embed)
        elif inp == "канал":
            if sett is None:
                await ctx.send("Вы не указали канал! Пример этой команды - *чат_а канал <упоминание канала>")
                return
            if sett in ctx.message.guild.channels:
                with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                    with db.cursor() as c:
                        c.execute(f"UPDATE guild SET chnlid = {sett.id} WHERE serverid = {ctx.message.guild.id}")
                        db.commit()
                        c.execute(f"SELECT enabled FROM guild WHERE serverid = {ctx.message.guild.id}")
                        b = c.fetchone()[0]
                        if b == "Disabled":
                            embed = disnake.Embed(title="**УСПЕШНО**",
                                    description=f'Канал теперь указан, НО межсерверный чат не включен. (пример - *чат_а переключить)',
                                    color=0x5900ff,
                                    timestamp=ctx.message.created_at)
                            await ctx.send(embed=embed)
                        else:
                            embed = disnake.Embed(title="**УСПЕШНО**",
                                    description=f'Канал теперь указан.',
                                    color=0x5900ff,
                                    timestamp=ctx.message.created_at)
                            await ctx.send(embed=embed)


    @commands.command(aliases=['чат', 'chat'])
    @has_permissions(administrator=True)
    @bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @pidor()
    async def __llllword(self, ctx):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                embed = disnake.Embed(title="**НАСТРОЙКИ ЧАТА**", color=0x7000cc, timestamp=ctx.message.created_at)
                c.execute(f"SELECT enabled FROM guild WHERE serverid = {ctx.message.guild.id}")
                maxwarnss = c.fetchone()[0]
                embed.add_field(
                            name=f"Включен ли межсерверный чат",
                            value=maxwarnss,
                            inline=True
                        )

                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {ctx.message.guild.id}")
                warnschannela = c.fetchone()[0]
                if warnschannela is None:
                    warnschannel = "Не указано"
                else:
                    a = self.bot.get_channel(warnschannela)
                    if a is not None:
                        
                        warnschannel = a.mention

                embed.add_field(
                            name=f"Канал для чата",
                            value=warnschannel,
                            inline=True
                        )
                servy = "Не указано"
                c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {ctx.message.guild.id}")
                serv = c.fetchone()[0]
                if serv is not None:
                    a = self.bot.get_guild(serv)
                    if a is not None:
                        
                        servy = f"{a.name} - {a.id}"


                embed.add_field(
                            name=f"Сопряженный сервер",
                            value=servy,
                            inline=True
                        )
                await ctx.send(embed=embed)












def setup(bot):
    bot.add_cog(chat(bot))