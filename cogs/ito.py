
from contextlib import closing
import random
import os
import string
import ssl
import disnake
from PIL import Image, ImageFont, ImageDraw
from disnake.ext import commands
from disnake.ext.commands import has_permissions
import asyncio
from email.message import EmailMessage
import psycopg2
import aiosmtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import qrcode
import smtplib
import requests
from dog_api import dog
from StringProgressBar import progressBar
from main import bot
import json
import subprocess
from rich.console import Console
from time import sleep
from config import password, host, db_name, bid
from disnake.enums import ButtonStyle
from config import user as userr
import re
from urllib.request import urlopen


MAIL_PARAMS = {'TLS': True, 'host': 'connect.smtp.bz', 'password': '2tkCS35k3DNN', 'user': 'support@heckerbot.ru', 'port': 587}

async def send_mail_async(sender, to, subject, text, textType='plain', **params):
    """Send an outgoing email with the given parameters.
    :param sender: From whom the email is being sent
    :type sender: str
    :param to: A list of recipient email addresses.
    :type to: list
    :param subject: The subject of the email.
    :type subject: str
    :param text: The text of the email.
    :type text: str
    :param textType: Mime subtype of text, defaults to 'plain' (can be 'html').
    :type text: str
    :param params: An optional set of parameters. (See below)
    :type params; dict
    Optional Parameters:
    :cc: A list of Cc email addresses.
    :bcc: A list of Bcc email addresses.
    """
    # Default Parameters
    cc = params.get("cc", [])
    bcc = params.get("bcc", [])
    mail_params = params.get("mail_params", MAIL_PARAMS)
    # Prepare Message
    msg = EmailMessage()
    msg.preamble = subject
    msg['Subject'] = subject
    msg['From'] = "support@heckerbot.ru"
    msg['To'] = to
    #if len(cc): msg['Cc'] = ', '.join(cc)
    #if len(bcc): msg['Bcc'] = ', '.join(bcc)
    msg.set_content(text)
    #msg.attach(MIMEText(text, textType, 'utf-8'))
    # Contact SMTP server and send Message
    host = mail_params.get('host')
    isSSL = mail_params.get('SSL', False);
    isTLS = mail_params.get('TLS', True);
    port = mail_params.get('port', 465 if isSSL else 25)
    context = ssl._create_unverified_context()

    smtp = aiosmtplib.SMTP(hostname="connect.smtp.bz", port=587)
    await smtp.connect()
    if 'user' in mail_params:
        await smtp.login(mail_params['user'], mail_params['password'])
    await smtp.send_message(msg)
    await smtp.quit()

class one(disnake.ui.View):
    msg: disnake.Message
    
    def __init__(self, usr, me, h):
        super().__init__(timeout=100)
        self.usr = usr
        self.ctx = me
        self.heck = h



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

    @disnake.ui.button(label="ДААА", style=ButtonStyle.red)
    async def first_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        self.children[0].disabled = True  # type: ignore
        self.children[1].disabled = True  # type: ignore
        try:
            await self.msg.edit(view=self)
        except:
            pass
        self.stop()

        ms = await self.ctx.send("Инициализация спутников...")
        await asyncio.sleep(3)
        await ms.edit(content="Инициализация спутников...Готово.")
        m1s = await self.ctx.send("Сбор первичной материи...")
        await asyncio.sleep(4)
        await m1s.edit(content="Сбор первичной материи...Готово.")
        m2s = await self.ctx.send("Преобразование активной первичной материи в статичную...")
        await asyncio.sleep(2)
        await m2s.edit(content="Преобразование активной первичной материи в статичную...Готово.")
        m3s = await self.ctx.send("Создание искуственного метеора из первичной материи...")
        await asyncio.sleep(5)
        await m3s.edit(content="Создание искуственного метеора из первичной материи...Готово.")
        m3s = await self.ctx.send(f"Поиск местоположения пользователя {self.usr.mention}...")
        await asyncio.sleep(5)
        await m3s.edit(content=f"Поиск местоположения пользователя {self.usr.mention}...Готово.")
        await self.ctx.send("Запуск через: 5")
        await asyncio.sleep(1)
        await self.ctx.send("4")
        await asyncio.sleep(1)
        await self.ctx.send("3")
        await asyncio.sleep(1)
        await self.ctx.send("2")
        await asyncio.sleep(1)
        await self.ctx.send("1")
        await asyncio.sleep(1)
        await self.ctx.send("Запуск инициализирован успешно!")
        await asyncio.sleep(1)
        await self.ctx.send("Через `5` секунд метеор достигнет цели.")
        await asyncio.sleep(5)
        try:
            await self.usr.send("https://img.wattpad.com/55e59356c4a76dc027abf1455c38bc65f19b1981/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f41466d62547374613274345330773d3d2d313131313830333337372e313661303366636233613963383131613539373033353537343639382e676966?s=fit&w=1280&h=1280")
            await self.usr.send(f"В вас запустил метеор {self.ctx.author.mention}")
        except:
            await self.ctx.send("Сообщение не удалось доставить, но")
        await self.ctx.send("Метеор доставлен!")

        
        

        
    @disnake.ui.button(label="нет", style=ButtonStyle.grey)
    async def not_first_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message("Ну, как хотите.")
        self.heck.reset_cooldown(self.ctx)
        self.children[0].disabled = True  # type: ignore
        self.children[1].disabled = True  # type: ignore
        try:
            await self.msg.edit(view=self)
        except:
            pass
        self.stop()
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
console = Console()
def shh():
    def predicate(ctx):
        if ctx.message.author.id not in bid:
            return False
        else:
            return True
    return commands.check(predicate)
def passw():
    async def predicate(ctx):
        
        await ctx.send("Пароль:")
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        try:

            message1 = await bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            embed = disnake.Embed(title="<:onno:954815596082659368>Извините<:onno:954815596082659368>",
                                  description=f"*Время ожидания вышло.*",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT pass FROM premium WHERE id = {ctx.message.author.id}")
                if message1.content != c.fetchone()[0]:
                    await ctx.send("Неверный пароль! Если вы забыли пароль, обратитесь на сервер поддержки для сброса.")
                    return False
                else:
                    return True
    return commands.check(predicate)
def pr():
    async def predicate(ctx):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT id FROM premium WHERE id = {ctx.author.id}")
                if c.fetchone() is None:
                    await ctx.send("Ишь какой хитрый! У тебя нет премиума для таких команд.")
                    return False
                else:
                    return True
        
    return commands.check(predicate)

async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()


class ito(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @shh()
    async def maill(self, ctx, to: str, title, text):
        await send_mail_async(
                  "support@heckerbot.ru",
                  to,
                  title,
                  text,
                  textType="plain")
        



    @commands.command()
    @pidor()
    @pr()
    async def ip(self, ctx, ip: str):
        async def ipInfo(addr=''):
            import socket
            from json import load
            addr = socket.gethostbyname(addr)
            if addr == '':
                url = 'https://ipinfo.io/json'
            else:
                url = 'https://ipinfo.io/' + addr + '/json'
            res = urlopen(url)
            #response from url(if res==None then check connection)
            data = load(res)
            #will load the json response into data
            list = []
            for attr in data.keys():
                #will print the data line by line
                #print(attr)
                #print(data[attr])
                print(attr,' '*1+'\t->\t',data[attr])
                #list.append(data[attr])
                if data[attr] != 'https://ipinfo.io/missingauth':
                    if attr == "ip":
                        a="IP"
                    if attr == "hostname":
                        a="Имя хоста"
                    if attr == "city":
                        a="Предположительный город"
                    if attr == "region":
                        a="Регион(область)"
                    if attr == "country":
                        a="Страна(ее код)"
                    if attr == "loc":
                        a="Местоположение(Широта-долгота)"
                    if attr == "org":
                        a="Организация"
                    if attr == "postal":
                        a="Код почты"
                    if attr == "timezone":
                        a="Временная зона"
                    list.append(f"{a} - {data[attr]}")
            try:
                '''if list[8] == 'https://ipinfo.io/missingauth':
                    embed = disnake.Embed(title="**Пробив**", description=f"IP - {list[0]}\nИмя хоста - {list[1]}\nПредположительный город - {list[2]}\nРегион(область) - {list[3]}\nСтрана - {list[4]}\nМестоположение(Широта-долгота) - {list[5]}\nОрганизация - {list[6]}\nВременная зона - {list[7]}")
                else:
                    embed = disnake.Embed(title="**Пробив**", description=f"IP - {list[0]}\nИмя хоста - {list[1]}\nПредположительный город - {list[2]}\nРегион(область) - {list[3]}\nСтрана - {list[4]}\nМестоположение(Широта-долгота) - {list[5]}\nОрганизация - {list[6]}\nПочтовый код - {list[7]}\nВременная зона - {list[8]}")
                await ctx.send(embed=embed)'''
                embedd = disnake.Embed(title="**Пробив**", description="** **")
                for n in list:
                    embedd.add_field(name=n, value="** **", inline=False)
                await ctx.send(embed=embedd)
            except:
                await ctx.send("Извините, найти информацию не удалось.")
        await ipInfo(ip)

    @commands.command()
    @shh()
    async def pon(self, ctx):
        a = disnake.utils.get(ctx.guild.stage_channels, name="Радио")
        vc = await a.connect()
        def repeat():

            audio = disnake.FFmpegPCMAudio('1.mp3')
            vc.play(audio, after=repeat())
        repeat()
            



    @commands.command()
    @shh()
    async def shell(self, ctx, *, tht):
        text = tht.split()
        useless_cat_call = subprocess.run(text, stdout=subprocess.PIPE, text=True)
        await ctx.send(useless_cat_call.stdout)
        print(useless_cat_call.stdout)  # Hello from the other side


    @commands.command()
    @shh()
    async def pispis(self, ctx):
        if "а" in ctx.message.author.name.lower():
            if len(ctx.message.author.name) > 5:
                await ctx.send("2 - Лол")
                
                return
            else:
                await ctx.send("14 - Норм")
                return
        if "о" in ctx.message.author.name.lower():
            if len(ctx.message.author.name) >= 6:
                await ctx.send("Вы не мужского пола! (-10)")
                return
            else:
                await ctx.send("13 - Нууу, сойдет")
                return
        elif "х" in ctx.message.author.name.lower():
            if len(ctx.message.author.name) > 5:
                await ctx.send("15 - Норм")
                return
            else:
                await ctx.send("63 - Иди, пиздуй во двор, понтуйся.")
                return
        
        elif "1" in ctx.message.author.name.lower():
            if "7" in ctx.message.author.name.lower():
                await ctx.send("1000-7 - 993?!?! Ты кто?")
                return

            if len(ctx.message.author.name) > 5:
                await ctx.send("16 - Норм")
                return
            else:
                await ctx.send("20 - Хорошо")
                return


    @commands.command()
    async def start(self, ctx):
        if ctx.author.voice is not None:
            if ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel.id
            else:
                await ctx.send("Зайдите в канал")
        else:
            await ctx.send("Зайдите в канал")
        link = await self.bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click the blue link!\n{link}")


    @commands.slash_command(name="server")
    @pidor()
    async def __serverinfo(self, inter: disnake.ApplicationCommandInteraction):
        """[Утилиты] - Информация о сервере"""
        embed=disnake.Embed(title=f"Информация о сервере {inter.guild.name}", color=0x008000)
        embed.add_field(name="Участники", value=f"Всего: {len(inter.guild.members)}\nИз них боты: {len(([member for member in inter.guild.members if member.bot]))}\nЛюди: {len(([member for member in inter.guild.members if not member.bot]))}", inline=True)
        embed.add_field(name="Каналы", value=f"Всего: {len(inter.guild.channels)}\nИз них голосовые: {len(inter.guild.voice_channels)}\nТекстовых: {len(inter.guild.text_channels)}", inline=True)
        embed.add_field(name="Создатель", value=f"{inter.guild.owner.name}#{inter.guild.owner.discriminator}", inline=True)
        embed.add_field(name="Дата создания сервера", value=f"год: {inter.guild.created_at.year}, месяц: {inter.guild.created_at.month}, день: {inter.guild.created_at.day}, {inter.guild.created_at.hour}:{inter.guild.created_at.minute}", inline=True)
        embed.add_field(name="Роли", value=len(inter.guild.roles), inline=True)
        if inter.guild.icon is not None:
            embed.set_thumbnail(url=inter.guild.icon.url)
        if inter.guild.banner is not None:
            embed.set_image(url=inter.guild.banner.url)
        await inter.response.send_message(embed=embed)

    @commands.command(aliases=["сервер", "serverinfo"])
    @pidor()
    async def __serverinfo(self, ctx):
        embed=disnake.Embed(title=f"Информация о сервере {ctx.guild.name}", color=0x008000)
        embed.add_field(name="Участники", value=f"Всего: {len(ctx.guild.members)}\nИз них боты: {len(([member for member in ctx.guild.members if member.bot]))}\nЛюди: {len(([member for member in ctx.guild.members if not member.bot]))}", inline=True)
        embed.add_field(name="Каналы", value=f"Всего: {len(ctx.guild.channels)}\nИз них голосовые: {len(ctx.guild.voice_channels)}\nТекстовых: {len(ctx.guild.text_channels)}", inline=True)
        embed.add_field(name="Создатель", value=f"{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}", inline=True)
        embed.add_field(name="Дата создания сервера", value=f"{ctx.guild.created_at.day}.{ctx.guild.created_at.month}.{ctx.guild.created_at.year}, {ctx.guild.created_at.hour}:{ctx.guild.created_at.minute}", inline=True)
        embed.add_field(name="Роли", value=len(ctx.guild.roles), inline=True)
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner is not None:
            embed.set_image(url=ctx.guild.banner.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['support', 'связь'])
    async def supp(self, ctx):
        embed=disnake.Embed(title=f"**Связь**", description="Информация для связи:\n\nПочта: supp@heckerbot.cf\nСервер поддержки: https://discord.gg/zJ9UnEkxEx", color=0x008000)
        await ctx.send(embed=embed)

    @commands.message_command()  # optional
    @pidor()
    async def Перевернуть(self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
        # Let's reverse it and send back
        await inter.response.defer()
        if message.content is None:
            await inter.followup.send("Сообщение пустое!")
            return
        try:
            await inter.followup.send(message.content[::-1])
        except:
            await inter.followup.send("У меня не вышло перевернуть сообщение!")
    @commands.message_command()  # optional
    @pidor()
    async def Перевод_раскладки(self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
        def from_ghbdtn(text):
            layout = dict(zip(map(ord, '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''),
                              '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'''))

            return text.translate(layout)

        await inter.response.send_message(str(from_ghbdtn(message.content)) + f" (Для {inter.author.mention})", ephemeral=True)



    @commands.slash_command(name="qr")
    @pidor()
    async def qrcode(self, inter: disnake.ApplicationCommandInteraction, inp):
        """[Фигня] - Создать qr код

        Parameters
        ----------
        inp: Текст, который нужно преобразовать
        """
        img = qrcode.make(inp)
        a: int = random.randint(1, 10000)
        img.save(f'{a}qr.png')
        await inter.response.send_message(file=disnake.File(f'{a}qr.png'))
        os.remove(f'{a}qr.png')

    @commands.slash_command()
    @pidor()
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        """[Утилиты] - Получить текущую задержку бота."""
        shard_id = inter.guild.shard_id
        shard = self.bot.get_shard(shard_id)

        embed = disnake.Embed(title=f"**ЗАДЕРЖКА**",
                            description=f"Общая задержка: {round(self.bot.latency * 1000)}мс\nЗадержка вашего шарда: {round(shard.latency * 1000)}мс\nВаш шард: {shard.id}\nКоличество серверов в вашем шарде: {len([guild for guild in self.bot.guilds if guild.shard_id == shard_id])}",
                            color=0x5900ff,
                            timestamp=inter.created_at)
        embed.set_author(name=f'heckerBOT', url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                         icon_url="https://cdn.discordapp.com/avatars/944890163975323728/36416ec401ad36dde8ddf01d2c1af9cc.png?size=256")
        await inter.response.send_message(embed=embed)

    @commands.command()
    @pidor()
    async def rub(self, ctx):
        data = requests.get('https://free.currconv.com/api/v7/convert?apiKey=f409c67e498a2e053408&q=USD_RUB&compact=ultra').json()
        await ctx.send(data['USD_RUB'])


    @commands.command()
    @shh()
    async def owners(self, ctx):

        e = '\n'.join([str(f"{server} - {str(server.owner.name)}") for server in self.bot.guilds])
        await ctx.send(f"Сейчас на {len(self.bot.guilds)} \n" + e + "\n")


    @commands.command()
    @shh()
    async def members(self, ctx):

        e = '\n'.join([str(f"{server} - {str(len(server.members))}") for server in self.bot.guilds])
        await ctx.send(f"Сейчас на {len(self.bot.users)} \n" + e + "\n")

        


    @commands.command()
    @pidor()
    async def qr(self, ctx, *, inp):
        img = qrcode.make(inp)
        a: int = random.randint(1, 10000)
        img.save(f'{a}qr.png')
        await ctx.send(file=disnake.File(f'{a}qr.png'))
        os.remove(f'{a}qr.png')

    @commands.slash_command(name='t2i')
    @pidor()
    async def __t2ii(self, inter: disnake.ApplicationCommandInteraction, bgcolor, textcolor, *, text):
        """[Фигня] - Текст в изображение

        Parameters
        ----------
        bgcolor: Цвет фона
        textcolor: Цвет текста
        text: Текст

        """
        if bgcolor == "пиво":
            await inter.response.send_message(file=disnake.File('25399.png'))
            return
        if bgcolor == "жёлтый":
            bgcolor = "yellow"
        if bgcolor == "желтый":
            bgcolor = "yellow"
        if bgcolor == "розовый":
            bgcolor = "pink"
        if bgcolor == "оранжевый":
            bgcolor = "orange"
        if bgcolor == "коричневый":
            bgcolor = "rgb(139,69,19)"
        if bgcolor == "голубой":
            bgcolor = "cyan"
        if bgcolor == "фиолетовый":
            bgcolor = "purple"
        if bgcolor == "серый":
            bgcolor = "gray"
        if bgcolor == "белый":
            bgcolor = "white"
        if bgcolor == "чёрный":
            bgcolor = "black"
        if bgcolor == "черный":
            bgcolor = "black"
        if bgcolor == "зелёный":
            bgcolor = "green"
        if bgcolor == "зеленый":
            bgcolor = "green"
        if bgcolor == "синий":
            bgcolor = "blue"
        if bgcolor == "красный":
            bgcolor = "red"

        if textcolor == "жёлтый":
            textcolor = "yellow"
        if textcolor == "желтый":
            textcolor = "yellow"
        if textcolor == "розовый":
            textcolor = "pink"
        if textcolor == "оранжевый":
            textcolor = "orange"
        if textcolor == "коричневый":
            textcolor = "rgb(139,69,19)"
        if textcolor == "голубой":
            textcolor = "cyan"
        if textcolor == "фиолетовый":
            textcolor = "purple"
        if textcolor == "серый":
            textcolor = "gray"
        if textcolor == "белый":
            textcolor = "white"
        if textcolor == "чёрный":
            textcolor = "black"
        if textcolor == "черный":
            textcolor = "black"
        if textcolor == "зелёный":
            textcolor = "green"
        if textcolor == "зеленый":
            textcolor = "green"
        if textcolor == "синий":
            textcolor = "blue"
        if textcolor == "красный":
            textcolor = "red"
        size = 300
        fnt = ImageFont.truetype("disneypark.ttf", size)
        image = Image.new(mode="RGB", size=(int(size / 2) * len(text), size + 50), color=bgcolor)
        draw = ImageDraw.Draw(image)
        # draw text
        draw.text((10, 10), text, font=fnt, fill=textcolor)
        # save file
        a = range(0, 100)
        h = random.choice(a)
        image.save(f"{h}.png")
        await inter.response.send_message(file=disnake.File(f'{h}.png'))
        os.remove(f'{h}.png')
        await inter.followup.send(f"Запросил {inter.author.mention}")
        


    @commands.command(aliases=['тви', 't2i'])
    @pidor()
    async def __t2i(self, ctx, bgcolor, textcolor, *, text):
        if bgcolor == "пиво":
            await ctx.send(file=disnake.File('25399.png'))
            return
        if bgcolor == "жёлтый":
            bgcolor = "yellow"
        if bgcolor == "желтый":
            bgcolor = "yellow"
        if bgcolor == "розовый":
            bgcolor = "pink"
        if bgcolor == "оранжевый":
            bgcolor = "orange"
        if bgcolor == "коричневый":
            bgcolor = "rgb(139,69,19)"
        if bgcolor == "голубой":
            bgcolor = "cyan"
        if bgcolor == "фиолетовый":
            bgcolor = "purple"
        if bgcolor == "серый":
            bgcolor = "gray"
        if bgcolor == "белый":
            bgcolor = "white"
        if bgcolor == "чёрный":
            bgcolor = "black"
        if bgcolor == "черный":
            bgcolor = "black"
        if bgcolor == "зелёный":
            bgcolor = "green"
        if bgcolor == "зеленый":
            bgcolor = "green"
        if bgcolor == "синий":
            bgcolor = "blue"
        if bgcolor == "красный":
            bgcolor = "red"

        if textcolor == "жёлтый":
            textcolor = "yellow"
        if textcolor == "желтый":
            textcolor = "yellow"
        if textcolor == "розовый":
            textcolor = "pink"
        if textcolor == "оранжевый":
            textcolor = "orange"
        if textcolor == "коричневый":
            textcolor = "rgb(139,69,19)"
        if textcolor == "голубой":
            textcolor = "cyan"
        if textcolor == "фиолетовый":
            textcolor = "purple"
        if textcolor == "серый":
            textcolor = "gray"
        if textcolor == "белый":
            textcolor = "white"
        if textcolor == "чёрный":
            textcolor = "black"
        if textcolor == "черный":
            textcolor = "black"
        if textcolor == "зелёный":
            textcolor = "green"
        if textcolor == "зеленый":
            textcolor = "green"
        if textcolor == "синий":
            textcolor = "blue"
        if textcolor == "красный":
            textcolor = "red"
        size = 300
        fnt = ImageFont.truetype("disneypark.ttf", size)
        image = Image.new(mode="RGB", size=(int(size / 2) * len(text), size + 50), color=bgcolor)
        draw = ImageDraw.Draw(image)
        # draw text
        draw.text((10, 10), text, font=fnt, fill=textcolor)
        # save file
        a = range(0, 100)
        h = random.choice(a)
        image.save(f"{h}.png")
        await ctx.send(file=disnake.File(f'{h}.png'))
        await ctx.send(f"Запросил {ctx.message.author.mention}")
        os.remove(f'{h}.png')


    @commands.slash_command(name='cat')
    @pidor()
    async def catt(self, inter: disnake.ApplicationCommandInteraction):
        """[Фигня] - Рандомный кот"""
        a = random.randint(1, 100)
        if a == 4:
            embed = disnake.Embed(title="**Поздравляем!**",
                                  description="Вам очень повезло! Шанс выпадения этой картинки - 1%! \n\nP.S. - Это кошка создателя!")
            await inter.response.send_message(embed=embed)
            await inter.followup.send('https://media.discordapp.net/attachments/731207671813767339/958025776282878012/1648481316683.jpg?width=613&height=670')
        else:
            responsee = requests.get('https://aws.random.cat/meow')
            data = responsee.json()

            await inter.response.send_message(data['file'])

    

    

    @commands.command(aliases=['cat', 'кот'])
    @pidor()
    async def __cat(self, ctx):
        a = random.randint(1, 100)
        if a == 4:
            embed = disnake.Embed(title="**Поздравляем!**",
                                  description="Вам очень повезло! Шанс выпадения этой картинки - 1%! \n\nP.S. - Это кошка создателя!")
            await ctx.send(embed=embed)
            await ctx.send('https://media.discordapp.net/attachments/731207671813767339/958025776282878012/1648481316683.jpg?width=613&height=670')
        else:
            response = requests.get('https://aws.random.cat/meow')
            data = response.json()

            await ctx.send(data['file'])
            
    @commands.command(aliases=['capybara', 'капибара'])
    @pidor()
    async def __capybara(self, ctx):
        response = requests.get('https://api.capybara-api.xyz/v1/image/random')
        data = response.json()
        await ctx.send(data['image_urls']['medium'])
    
    @commands.slash_command()
    @pidor()
    async def капибара(self, inter: disnake.ApplicationCommandInteraction):
        """[Фигня] - Рандомная капибара"""
        await inter.response.defer()
        response = requests.get('https://api.capybara-api.xyz/v1/image/random')
        data = response.json()
        await inter.followup.send(data['image_urls']['medium'])

    @commands.slash_command(name='dog')
    @pidor()
    async def dooog(self, inter: disnake.ApplicationCommandInteraction):
        """[Фигня] - Рандомная собака"""
        await inter.response.send_message(dog.random_image())

    @commands.command(aliases=['dog', 'собака'])
    @pidor()
    async def __cj(self, ctx):
        await ctx.send(dog.random_image())

    @commands.slash_command(name="ben")
    @pidor()
    async def __benn(self, inter: disnake.ApplicationCommandInteraction, q=None):
        """[Фигня] - Спроси бена"""
        word_ben = ['*Упал со стула*', 'Ho Ho Ho', 'Bueee', 'Yees', 'No', '*Положил трубку*']
        await inter.response.send_message(random.choice(word_ben))

    @commands.command(aliases=['ben', 'бен'])
    @pidor()
    async def __ben(self, ctx):
        word_ben = ['*Упал со стула*', 'Ho Ho Ho', 'Bueee', 'Yees', 'No', '*Положил трубку*']
        await ctx.send(random.choice(word_ben))

    @commands.group()
    @pr()
    @commands.guild_only()
    async def sudo(self, ctx):
        
        if ctx.invoked_subcommand is None:
            await ctx.send('usage: sudo -h | -K | -k | -V\nusage: sudo -v [-ABknS] [-g group] [-h host] [-p prompt] [-u user]\nusage: sudo -l [-ABknS] [-g group] [-h host] [-p prompt] [-U user] [-u user] [command]\nusage: sudo [-ABbEHknPS] [-r role] [-t type] [-C num] [-D directory] [-g group] [-h host] [-p prompt] [-R directory] [-T timeout] [-u user] [VAR=value] [-i|-s] [<command>]\nusage: sudo -e [-ABknS] [-r role] [-t type] [-C num] [-D directory] [-g group] [-h host] [-p prompt] [-R directory] [-T timeout] [-u user] file ...')




    @sudo.command()
    @passw()
    @commands.cooldown(1, 100, commands.BucketType.guild)
    async def apt(self, ctx, *, args = None):
        if args is None:
            await ctx.send("apt 2.4.8 (amd64)\nИспользование: apt [параметры] команда\n\napt — менеджер пакетов с интерфейсом командной строки. Он предоставляет\nкоманды для поиска и управления, а также запросов информации о пакетах.\napt выполняет те же задачи, что и специализированные инструменты APT,\nнапример apt-get и apt-cache, но по умолчанию задействует параметры,\nкоторые больше подходят для интерактивного использования.\n\nОсновные команды:\n  install - установить пакеты\n  remove - удалить пакеты\nДополнительную информацию о доступных командах смотрите в apt(8).\nПараметры настройки и синтаксис описаны в apt.conf(5).\nИнформацию о том, как настроить источники, можно найти в sources.list(5).\nВыбор пакетов и версий описывается в apt_preferences(5).\nИнформация о безопасности доступна в apt-secure(8).\n                    В APT есть коровья СУПЕРСИЛА.\n")
            self.apt.reset_cooldown(ctx)
        elif args == "install heck":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
            
                    msg = await ctx.send("Чтение списков пакетов…")
                    await msg.edit(content="Чтение списков пакетов… Готово")
                    msg2 = await ctx.send("Построение дерева зависимостей…")
                    await msg2.edit(content="Построение дерева зависимостей… Готово")
                    msg3 = await ctx.send("Чтение информации о состоянии…")
                    await msg3.edit(content="Чтение информации о состоянии… Готово")
                    c.execute(f"SELECT heckjopa FROM server WHERE id = {ctx.guild.id}")
                    if c.fetchone()[0] == 'Yes':
                        await ctx.send("Уже установлен пакет heck самой новой версии (1.4.0-1).\nОбновлено 0 пакетов, установлено 0 новых пакетов, для удаления отмечено 0 пакетов.")
                        self.apt.reset_cooldown(ctx)
                        return
                    await ctx.send("Следующие НОВЫЕ пакеты будут установлены:\n heck autoconf automake autopoint autotools-dev debhelper debugedit\n dh-autoreconf dh-strip-nondeterminism dwz libarchive-cpio-perl\n libdebhelper-perl libfile-stripnondeterminism-perl libltdl-dev\n libmail-sendmail-perl librpm9 librpmbuild9 librpmio9 librpmsign9\n libsub-override-perl libsys-hostname-long-perl libtool m4 po-debconf rpm\n rpm-common rpm2cpio")
                    await ctx.send("Обновлено 0 пакетов, установлено 27 новых пакетов, для удаления отмечено 0 пакетов, и 0 пакетов не обновлено.\n Необходимо скачать 16,6 MB архивов.\n После данной операции объём занятого дискового пространства возрастёт на 24,1 MB.\n Хотите продолжить? [Д/н]")
                    def check(m):
                        return m.channel == ctx.channel and m.author == ctx.author

                    message = await self.bot.wait_for('message', check=check, timeout=60)
                    yep = ["y", "yes", "д", "да"]

                    if message.content.lower() in yep:
                        await ctx.send("Пол:1 http://deb.debian.org/debian bullseye/main amd64 autotools-dev all 20180224.1+nmu1 [77,1 kB]\nПол:2 http://deb.debian.org/debian bullseye/main amd64 m4 amd64 1.4.18-5 [204 kB]\nПол:3 http://deb.debian.org/debian bullseye/main amd64 autoconf all 2.69-14 [313 kB]\nПол:4 http://deb.debian.org/debian bullseye/main amd64 automake all 1:1.16.3-2 [814 kB]\nПол:5 http://deb.debian.org/debian bullseye/main amd64 autopoint all 0.21-4 [510 kB]\nПол:6 http://deb.debian.org/debian bullseye/main amd64 libdebhelper-perl all 13.3.4 [189 kB]\nПол:7 http://deb.debian.org/debian bullseye/main amd64 libtool all 2.4.6-15 [513 kB]\nПол:8 http://deb.debian.org/debian bullseye/main amd64 dh-autoreconf all 20 [17,1 kB]\nПол:9 http://deb.debian.org/debian bullseye/main amd64 libsub-override-perl all 0.09-2 [10,2 kB]")

                        await ctx.send("Пол:10 http://deb.debian.org/debian bullseye/main amd64 libfile-stripnondeterminism-perl all 1.12.0-1 [26,3 kB]\nПол:11 http://deb.debian.org/debian bullseye/main amd64 dh-strip-nondeterminism all 1.12.0-1 [15,4 kB]\nПол:12 http://deb.debian.org/debian bullseye/main amd64 dwz amd64 0.13+20210201-1 [175 kB]\nПол:13 http://deb.debian.org/debian bullseye/main amd64 po-debconf all 1.0.21+nmu1 [248 kB]\nПол:14 http://deb.debian.org/debian bullseye/main amd64 debhelper all 13.3.4 [1,049 kB]\nПол:15 http://deb.debian.org/debian bullseye/main amd64 librpmio9 amd64 4.16.1.2+dfsg1-3 [1,530 kB]\nПол:16 http://deb.debian.org/debian bullseye/main amd64 librpm9 amd64 4.16.1.2+dfsg1-3 [1,630 kB]\nПол:17 http://deb.debian.org/debian bullseye/main amd64 librpmbuild9 amd64 4.16.1.2+dfsg1-3 [1,523 kB]\nПол:18 http://deb.debian.org/debian bullseye/main amd64 librpmsign9 amd64 4.16.1.2+dfsg1-3 [1,457 kB]\nПол:19 http://deb.debian.org/debian bullseye/main amd64 rpm-common amd64 4.16.1.2+dfsg1-3 [1,479 kB]\nПол:20 http://deb.debian.org/debian bullseye/main amd64 rpm2cpio amd64 4.16.1.2+dfsg1-3 [1,458 kB]\nПол:21 http://deb.debian.org/debian bullseye/main amd64 debugedit amd64 4.16.1.2+dfsg1-3 [1,472 kB]")
                        
                        await ctx.send("Пол:22 http://deb.debian.org/debian bullseye/main amd64 rpm amd64 4.16.1.2+dfsg1-3 [1,576 kB]\nПол:23 http://deb.debian.org/debian bullseye/main amd64 heck all 8.95.4 [77,8 kB]\nПол:24 http://deb.debian.org/debian bullseye/main amd64 libarchive-cpio-perl all 0.10-1.1 [10,6 kB]\nПол:25 http://deb.debian.org/debian bullseye/main amd64 libltdl-dev amd64 2.4.6-15 [162 kB]\nПол:26 http://deb.debian.org/debian bullseye/main amd64 libsys-hostname-long-perl all 1.5-2 [11,8 kB]\nПол:27 http://deb.debian.org/debian bullseye/main amd64 libmail-sendmail-perl all 0.80-1.1 [25,5 kB]")
                        total = 100
                        current = 0
                        # First two arguments are mandatory
                        bardata = progressBar.filledBar(total, round(current))
                        # Get the progressbar
                        a = await ctx.send(content=f"Скачивание:{bardata[1]} {bardata[0]}")
                        while current < total:

                            current += int(random.randint(1, 3))
                            bardata = progressBar.filledBar(total, round(current))
                            await a.edit(content=f"Скачивание: {round(current)}% {bardata[0]}")
                        if current == 98:
                            current += 2
                        if current == 99:
                            current += 1
                        if current == 97:
                            current += 3
                            
                        await a.edit(content=f"Скачивание: 100% {bardata[0]}")

                        await ctx.send("Скачивание завершено.")

                        total1 = 100
                        current1 = 0
                        # First two arguments are mandatory
                        bardata1 = progressBar.filledBar(total1, round(current1))
                        # Get the progressbar
                        a = await ctx.send(f"Распаковка пакетов: {bardata1[1]}% {bardata1[0]}")
                        while current1 < total1:
                            current1 += int(random.randint(1, 3))
                            bardata1 = progressBar.filledBar(total1, round(current1))
                            await a.edit(content=f"Распаковка пакетов: {round(current1)}% {bardata1[0]}")
                        if current1 == 98:
                            current1 += 2
                        if current1 == 99:
                            current1 += 1
                        if current1 == 97:
                            current1 += 3
                        await a.edit(content=f"Скачивание: 100% {bardata1[0]}")

                        await ctx.send("Распаковка завершена.")
                        s = await ctx.send("Установка")
                        await s.edit(content=f"Установка.")
                        await s.edit(content=f"Установка..")
                        await s.edit(content=f"Установка...")
                        await s.edit(content=f"Установка.")
                        await s.edit(content=f"Установка..")
                        await s.edit(content=f"Установка...")
                        c.execute(f"UPDATE server SET heckjopa = 'Yes' WHERE id = {ctx.guild.id}")
                        db.commit()

                        await ctx.send('Установка пакета "heck" завершена.')
                    else:
                        await ctx.send("Скачивание отменено.")
                        self.apt.reset_cooldown(ctx)
                        return
        elif args == "install":
            msg = await ctx.send("Чтение списков пакетов…")
            await msg.edit(content="Чтение списков пакетов… Готово")
            msg2 = await ctx.send("Построение дерева зависимостей…")
            await msg2.edit(content="Построение дерева зависимостей… Готово")
            msg3 = await ctx.send("Чтение информации о состоянии…")
            await msg3.edit(content="Чтение информации о состоянии… Готово")
            await ctx.send("Обновлено 0 пакетов, установлено 0 новых пакетов, для удаления отмечено 0 пакетов.")
            self.apt.reset_cooldown(ctx)
            return
        elif args == "remove":
            msg = await ctx.send("Чтение списков пакетов…")
            await msg.edit(content="Чтение списков пакетов… Готово")
            msg2 = await ctx.send("Построение дерева зависимостей…")
            await msg2.edit(content="Построение дерева зависимостей… Готово")
            msg3 = await ctx.send("Чтение информации о состоянии…")
            await msg3.edit(content="Чтение информации о состоянии… Готово")
            await ctx.send("Обновлено 0 пакетов, установлено 0 новых пакетов, для удаления отмечено 0 пакетов.")
            self.apt.reset_cooldown(ctx)
            return
        elif args == "remove heck":
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    msg = await ctx.send("Чтение списков пакетов…")
                    await msg.edit(content="Чтение списков пакетов… Готово")
                    msg2 = await ctx.send("Построение дерева зависимостей…")
                    await msg2.edit(content="Построение дерева зависимостей… Готово")
                    msg3 = await ctx.send("Чтение информации о состоянии…")
                    await msg3.edit(content="Чтение информации о состоянии… Готово")
                    c.execute(f"SELECT heckjopa FROM server WHERE id = {ctx.guild.id}")
                    if c.fetchone()[0] == 'No':
                        await ctx.send("Пакет «heck» не установлен, поэтому не может быть удалён\nОбновлено 0 пакетов, установлено 0 новых пакетов, для удаления отмечено 0 пакетов.\n")
                        self.apt.reset_cooldown(ctx)
                        return
                    await ctx.send("Следующие пакеты будут УДАЛЕНЫ:\n heck\nОбновлено 0 пакетов, установлено 0 новых пакетов, для удаления отмечено 1 пакетов.\nПосле данной операции объём занятого дискового пространства уменьшится на 24,1 MB.")
                    await ctx.send("Хотите продолжить? [Д/н]")
                    def check(m):
                        return m.channel == ctx.channel and m.author == ctx.author

                    message = await self.bot.wait_for('message', check=check, timeout=60)
                    yep = ["y", "yes", "д", "да"]
                    if message.content.lower() in yep:
                        mss = await ctx.send("(Чтение базы данных … )")
                        await mss.edit(content="(Чтение базы данных … на данный момент установлено 254649 файлов и каталогов.)")
                        s = await ctx.send("Удаляется heck")
                        await s.edit(content=f"Удаляется heck.")
                        await s.edit(content=f"Удаляется heck..")
                        await s.edit(content=f"Удаляется heck...")
                        await s.edit(content=f"Удаляется heck.")
                        await s.edit(content=f"Удаляется heck..")
                        await s.edit(content=f"Удаляется heck...")
                        await ctx.send("Обрабатываются триггеры для man-db (2.10.2-1) …")
                        await asyncio.sleep(3)
                        c.execute(f"UPDATE server SET heckjopa = 'No' WHERE id = {ctx.guild.id}")
                        db.commit()
                        await ctx.send('Пакет "heck" удален.')
                    else:
                        self.apt.reset_cooldown(ctx)
                        await ctx.send("Удаление отменено.")
                        return
        else:
            self.apt.reset_cooldown(ctx)
            await ctx.send("Команда не распознана.")

    @sudo.command()
    @passw()
    @commands.cooldown(1, 150, commands.BucketType.guild)
    async def heck(self, ctx, *, args = None):
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT heckjopa FROM server WHERE id = {ctx.guild.id}")
                if c.fetchone()[0] == 'No':
                    await ctx.send("Команда «heck» не найдена, но может быть установлена с помощью:\nsudo apt install heck")
                    self.heck.reset_cooldown(ctx)
                    return
                if args is None:
                    await ctx.send("Предоставляемые услуги: \n\nheck jopa;\nheck pentagon (в разработке);\nheck airstrike(в разработке);\nheck meteor.")
                    self.heck.reset_cooldown(ctx)
                elif args == "jopa":
                    c.execute(f"SELECT FROM jopa_heck WHERE id = {ctx.guild.id}")
                    if c.fetchone() is not None:
                        await ctx.send("Данная команда заблокирована на этом сервере!")
                        self.heck.reset_cooldown(ctx)
                        return

                    def check(m):
                        return m.channel == ctx.channel and m.author == ctx.author
                    await ctx.send("Здравствуйте!, вас приветствует САМАЯ ПРАВДОПОДОБНАЯ утилита 'Взлом жопы'.\nУпоминание цели для взлома:")
                    message3 = await self.bot.wait_for('message', check=check, timeout=60)
                    if len(message3.content) < 6:
                        await ctx.send("Такого пользователя нет!")
                        return
                    f: int = int(message3.content[2:-1])
                    myaccount: disnake.User = self.bot.get_user(f)
                    if myaccount is None:
                        await ctx.send("Такого пользователя нет!")
                        self.heck.reset_cooldown(ctx)
                        return
                    if myaccount.id == ctx.message.author.id:
                        await ctx.send("Себя ломать нельзя!")
                        self.heck.reset_cooldown(ctx)
                        return
                    if myaccount.bot:
                        await ctx.send("Ботов ломать низя!")
                        self.heck.reset_cooldown(ctx)
                        return


                    total2 = 100
                    current2 = 0
                    # First two arguments are mandatory
                    bardata2 = progressBar.filledBar(total2, current2)
                    # Get the progressbar
                    a = await ctx.send(f"Взлом жопы участника {myaccount.mention}: {bardata2[1]}% {bardata2[0]}")
                    while current2 < total2:

                        await asyncio.sleep(0.4)
                        current2 += int(random.randint(1, 3))
                        bardata2 = progressBar.filledBar(total2, round(current2))
                        await a.edit(content=f"Взлом жопы участника {myaccount.mention}: {round(bardata2[1])}% {bardata2[0]}")
                    await a.edit(content=f"Взлом жопы участника {myaccount.mention}: 100% {bardata2[0]}")


                    v = ctx.message.author
                    pas = ''
                    for x in range(random.randint(8, 16)): #Количество символов (16)
                        pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
                    
                    crea = f"год: {myaccount.created_at.year}, месяц: {myaccount.created_at.month}, день: {myaccount.created_at.day}, {myaccount.created_at.hour}:{myaccount.created_at.minute}"
                    await v.send(f"Данные:\n\n{myaccount.mention}\nПочта:||mihail.bebra@gmail.com||\nПароль:||{str(pas)}||\nДата создания аккаунта: {crea}")

                    await ctx.send("Взлом жопы завершен. Данные участника отправлены в лс.")
                elif args == "meteor":
                    c.execute(f"SELECT FROM jopa_heck WHERE id = {ctx.guild.id}")
                    if c.fetchone() is not None:
                        await ctx.send("Данная команда заблокирована на этом сервере!")
                        self.heck.reset_cooldown(ctx)
                        return

                    def check(m):
                        return m.channel == ctx.channel and m.author == ctx.author
                    await ctx.send("Здравствуйте!, вас приветствует САМАЯ ПРАВДОПОДОБНАЯ утилита 'Метеор'.\nУпоминание цели для отправки метеора:")

                    message3 = await self.bot.wait_for('message', check=check, timeout=60)
                    if len(message3.content) < 6:
                        await ctx.send("Такого пользователя нет!")
                        self.heck.reset_cooldown(ctx)
                        return
                    f: int = int(message3.content[2:-1])
                    myaccount: disnake.User = self.bot.get_user(f)
                    if myaccount is None:
                        await ctx.send("Такого пользователя нет!")
                        self.heck.reset_cooldown(ctx)
                        return
                    if myaccount.id == ctx.message.author.id:
                        await ctx.send("Себя нельзя!")
                        self.heck.reset_cooldown(ctx)
                        return
                    if myaccount.bot:
                        await ctx.send("Ботов низя!")
                        self.heck.reset_cooldown(ctx)
                        return
                    view = one(myaccount, ctx, self.heck)
                    view.msg = await ctx.send("Вы уверены? Нажмите на большую красную кнопку для продолжения.", view=view)

                elif args == "pentagon":
                    c.execute(f"SELECT FROM jopa_heck WHERE id = {ctx.guild.id}")
                    if c.fetchone() is not None:
                        await ctx.send("Данная команда заблокирована на этом сервере!")
                        self.heck.reset_cooldown(ctx)
                        return
                    
                else:
                    self.heck.reset_cooldown(ctx)
                    await ctx.send("Неизвестный аргумент.")






    

                


def setup(bot):
    bot.add_cog(ito(bot))
