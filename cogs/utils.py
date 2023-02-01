from contextlib import closing
import disnake
from disnake.ext import commands
import psycopg2
from config import bid
import random
import asyncio
from config import password, host, db_name, bid
from StringProgressBar import progressBar
from config import user as userr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
from rich.console import Console
from time import sleep
from rich.markdown import Markdown
console = Console()
import smtplib



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
def shh():
    def predicate(ctx):
        if ctx.message.author.id not in bid:
            return False
        else:
            return True
    return commands.check(predicate)

class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['hdgf'])
    async def __sd(self, ctx):
        if ctx.message.author.id not in bid:
            return
        await ctx.channel.purge(limit=1)
        embed = disnake.Embed(title="**Обновление**",
                              description='@everyone\n\nТеперь ник бота heckerBOT',
                              color=0x008000)
        embed.set_author(name="heckerBOT",
                         icon_url="https://cdn.discordapp.com/avatars/944890163975323728/36416ec401ad36dde8ddf01d2c1af9cc.png?size=256")
        await ctx.send(embed=embed)

    @commands.slash_command(name='avatar')
    @pidor()
    async def __avaaa(self, inter: disnake.ApplicationCommandInteraction, member: disnake.User = None):
        """[Утилиты] - Отправляет аватар пользователя"""
        if member is None:
            usr: disnake.User = inter.author
            if usr.avatar is None:
                await inter.response.send_message("У пользователя нет аватара!")
            await inter.response.send_message(usr.avatar.url)
        else:
            if member.avatar is None:
                await inter.response.send_message("У пользователя нет аватара!")
            await inter.response.send_message(member.avatar.url)
    
    @commands.command()
    @shh()
    async def mail(self, ctx, to: str, *, text: str):
        smtp = smtplib.SMTP_SSL()
        smtp.connect('smtp.mail.com', 465)
        smtp.starttls()
        smtp.login('supp@heckerbot.cf','Vm89517259298')
        msg = f'''
        From: heckerbot support
        Subject: TEST

        {text}
        '''
        smtp.sendmail("supp@heckerbot.cf", to, msg)
        await ctx.send("DONE")
        smtp.quit()


    @commands.user_command()
    @pidor()
    async def Аватар(self, inter: disnake.ApplicationCommandInteraction, member: disnake.User = None):
        if member is None:
            usr: disnake.User = inter.author
            if usr.avatar is None:
                await inter.response.send_message("У пользователя нет аватара!")
            await inter.response.send_message(usr.avatar.url)
        else:
            if member.avatar is None:
                await inter.response.send_message("У пользователя нет аватара!")
            await inter.response.send_message(member.avatar.url)

    @commands.command(aliases=['avatar', 'аватар'])
    @pidor()
    async def __ava(self, ctx, avamember: disnake.User = None):
        if avamember is None:
            usr: disnake.User = ctx.message.author
            await ctx.send(usr.avatar.url)
        else:
            await ctx.send(avamember.avatar.url)

    @commands.slash_command(aliases=['coin', 'монетка'])
    @pidor()
    async def __coin(self, inter: disnake.ApplicationCommandInteraction):
        """[Утилиты] - Подбросьте монетку!"""
        st = [1, 2]
        if random.choice(st) == 1:
            m = "Решка"
        else:
            m = "Орел"
        await inter.response.send_message(m)   

    @commands.command(aliases=['coin', 'монетка'])
    @pidor()
    async def __coin(self, ctx):
        st = [1, 2]
        if random.choice(st) == 1:
            m = "Решка"
        else:
            m = "Орел"
        await ctx.send(m)



    @commands.command(aliases=['tr', 'перевод'])
    @pidor()
    async def __tr(self, ctx, *, text):
        def from_ghbdtn(text):
            layout = dict(zip(map(ord, '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''),
                              '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'''))

            return text.translate(layout)

        await ctx.send(str(from_ghbdtn(text)) + f" (Для {ctx.author.mention})")
    
    @commands.command()
    @shh()
    @pidor()
    async def aa(self, ctx):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                """c.execute("SELECT id FROM premium")
                hah = c.fetchall()
                for id in hah:
                    mem = self.bot.get_guild(844649033502818314).get_member(id[0])
                    if mem in self.bot.get_guild(844649033502818314).members:
                        role = self.bot.get_guild(844649033502818314).get_role(1037770212004605972)
                        if role in mem.roles:
                            pass
                        else:
                            await mem.add_roles(role)"""
                c.execute("SELECT chnlid, serverid FROM guild WHERE chnlid IS NOT NULL")
                a = c.fetchall()
                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author
                await ctx.send("Введите название эмбеда:")

                title1 = await self.bot.wait_for('message', check=check, timeout=60)
                title = title1.content
                await ctx.send("Введите содержание эмбеда:")

                msg1 = await self.bot.wait_for('message', check=check, timeout=180)
                msg = msg1.content
                
                total = len(a)
                current = 0
                # First two arguments are mandatory
                bardata = progressBar.filledBar(total, current)
                b = await ctx.send(content=f"Прогресс:{bardata[1]} {bardata[0]}")
                # Get the progressbar
                for m in a:
                    guildtu = self.bot.get_guild(m[1])
                    chnl = self.bot.get_channel(m[0])
                    
                    
                    if guildtu is not None:
                        if chnl in guildtu.channels:
                            
                            try:
                                


                                embedd = disnake.Embed(title=title,
                                    description=msg,
                                    color=0x5900ff,
                                    timestamp=ctx.message.created_at)
                                embedd.set_author(name="хекер", url="https://discord.gg/PvRHYF4djp",
                            icon_url="https://cdn.discordapp.com/avatars/944890163975323728/36416ec401ad36dde8ddf01d2c1af9cc.png?size=256")
                                await chnl.send(embed=embedd)
                                current += 1
                                bardata = progressBar.filledBar(total, current)
                                await b.edit(content=f"Прогресс: {current}/{len(a)} {bardata[0]}")
                            except Exception:
                                console.print_exception(show_locals=True)

                await ctx.send("Готово!")

                    

                    

    


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"DELETE FROM server WHERE id = {guild.id}")
                c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {guild.id}")
                a = c.fetchone()
                if a is not None:
                    if a[0] != 0:
                        c.execute(f"UPDATE guild SET serveridtu = 0 WHERE serveridtu = {guild.id}")
                c.execute(f"SELECT serverid FROM banned WHERE serverid = {guild.id}")
                if c.fetchone() is not None:
                    c.execute(f"DELETE FROM banned WHERE serverid = {guild.id}")

                c.execute(f"SELECT serverid FROM bannedg WHERE serverid = {guild.id}")
                if c.fetchone() is not None:
                    c.execute(f"DELETE FROM bannedg WHERE serverid = {guild.id}")
                c.execute(f"DELETE FROM guild WHERE serverid = {guild.id}")
                c.execute(f"SELECT roleid FROM shop WHERE serverid = {guild.id}")

                if c.fetchone() is not None:
                    c.execute(f"DELETE FROM shop WHERE serverid = {guild.id}")
                db.commit()
                with console.status("[bold red]Удаляем сервер из БД...") as status:


                    c.execute(f"DELETE FROM users WHERE serverid = {guild.id}")
                    console.log(f"[bold][magenta]Удален сервер - [/magenta]{guild.name}")

                    db.commit()  # применение изменений в БД
                
                channel = self.bot.get_channel(844942954800087101)
                await channel.send('Минус( "' + str(guild) + '"')

    @commands.command(aliases=['пинг', 'ping'])
    @pidor()
    async def __пинг(self, ctx):
        shard_id = ctx.guild.shard_id
        shard = self.bot.get_shard(shard_id)

        embed = disnake.Embed(title=f"**ЗАДЕРЖКА**",
                            description=f"Общая задержка: {round(self.bot.latency * 1000)}мс\nЗадержка вашего шарда: {round(shard.latency * 1000)}мс\nВаш шард: {shard.id}\nКоличество серверов в вашем шарде: {len([guild for guild in self.bot.guilds if guild.shard_id == shard_id])}",
                            color=0x5900ff,
                            timestamp=ctx.message.created_at)
        embed.set_author(name=f'heckerBOT', url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                         icon_url="https://cdn.discordapp.com/avatars/944890163975323728/36416ec401ad36dde8ddf01d2c1af9cc.png?size=256")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(utils(bot))
