import asyncio
from asyncio import exceptions, TimeoutError
from contextlib import closing
from datetime import datetime, timezone
import disnake
from disnake.ext import commands
from config import bid
import random
import math
import psycopg2
from disnake.ext.commands import has_permissions
import subprocess
import time
from rich.traceback import install
install(show_locals=True)
from config import password, host, db_name, token, bid
from config import user as userr

from rich.console import Console
from time import sleep
from rich.markdown import Markdown
console = Console()

def human_join(iterable, delim=', ', *, final='and'):
    """Joins an iterable in a human-readable way.

    The items are joined such that the last two items will be joined with a
    different delimiter than the rest.
    """

    seq = tuple(iterable)
    if not seq:
        return ''

    return f"{delim.join(seq[:-1])} {final} {seq[-1]}" if len(seq) != 1 else seq[0]

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

def del_fr_us(id: int, gid: int):
    db = psycopg2.connect(host=host, user=userr, password=password, database=db_name)
    c = db.cursor()
    try:
        c.execute(f"DELETE FROM users WHERE userid = {id} AND serverid = {gid}")  # вводит все данные об участнике в БД
        db.commit()
    except:
        c.execute("ROLLBACK")
        db.commit()
    finally:
        c.close()
        db.close()



class BButton(disnake.ui.Button):
    def __init__(self, style: disnake.ButtonStyle, label: str, custom_id: str):
        super().__init__(style=style, label=label, disabled=False, custom_id=custom_id)
        self.style = style
        self.value = label
        self.custom_id = custom_id

    async def callback(self, interaction: disnake.Interaction):
        # логика

        if self.label == '1':
            embed = disnake.Embed(title="**МОДЕРИРОВАНИЕ**",
                                  description="**Внимание! Перед командой ставьте звездочку!\nФормат объяснения - первое название команды, второе название - объяснение, пример использования команды с аргументами/без**\n\n`Бан`, `ban` - Забанить пользователя, `бан <упоминание пользователя> <причина (необязательно)>`\n\n`Кик`, `kick` - Кикнуть пользователя, `кик <упоминание пользователя> <причина (необязательно)>`\n\n`Мут`, `mute` - Замутить пользователя (тайм аут), `мут <упоминание пользователя> <время мута в минутах> <причина (необязательно)>`\n\n`Очистить`, `clear` - Очистить н-ое количество сообщений, `очистить <кол-во сообщений>`",
                                  color=0x7300ff)
            embed.set_author(name="heckerBOT", url="https://discord.gg/PvRHYF4djp",
                             icon_url="https://cdn.discordapp.com/avatars/944890163975323728/e795126f4bed13c0348ae3dd69cc44d4.png?size=1024")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.label == '2':
            embed = disnake.Embed(title="**УТИЛИТЫ**",
                                  description="**Внимание! Перед командой ставьте звездочку!\nФормат объяснения - первое название команды, второе название - объяснение, пример использования команды с аргументами/без**\n\n`Пинг`, `ping` - Проверка реакции бота, `пинг`\n\n`Перевод`, `tr` - Перевод текста с английской раскладки, на русскую, `перевод <текст>`\n\n`Аватар`, `avatar` - Дает вам ссылку на аватар пользователя, `аватар <упоминание пользователя>`\n\n`Монетка`, `coin` - Подбросьте монетку!, `монетка`\n\n`Сервер`, `serverinfo` - Покажет информацию о сервере, `сервер`\n\n`Support`, `связь` - Информация для связи с поддержкой, `связь`",
                                  color=0x7300ff)
            embed.set_author(name="heckerBOT", url="https://discord.gg/PvRHYF4djp",
                             icon_url="https://cdn.discordapp.com/avatars/944890163975323728/e795126f4bed13c0348ae3dd69cc44d4.png?size=1024")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.label == '3':
            embed = disnake.Embed(title="**ВЕЩИ СДЕЛАННЫЕ ПРОСТО ТАК И НЕ ИМЕЮЩИЕ СМЫСЛА**",
                                  description="**Внимание! Перед командой ставьте звездочку!\nФормат объяснения - первое название команды, второе название - объяснение, пример использования команды с аргументами/без**\n\n`Бен`, `ben` - Вопрос Бену(рандом), `бен <вопрос>`\n\n`Капибара`, `capybara` - Рандомная капибара, `капибара`\n\n`Кот`, `cat` - Рандомный кот (есть пасхалка), `кот`\n\n`Собака`, `dog` - Рандомная собака, `собака`\n\n`Тви`, `t2i` - Преобразование текста в изображение, `тви <цвет фона> <цвет текста> <текст>`\n\n`Qr` - Преобразование текста в qr код, `qr <текст>`",
                                  color=0x7300ff)
            embed.set_author(name="heckerBOT", url="https://discord.gg/PvRHYF4djp",
                             icon_url="https://cdn.discordapp.com/avatars/944890163975323728/e795126f4bed13c0348ae3dd69cc44d4.png?size=1024")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.label == '4':
            embed = disnake.Embed(title="**ЭКОНОМИКА И ВСЁ СОПУТСТВУЮЩЕЕ**",
                                  description="**Внимание! Перед командой ставьте звездочку!\nФормат объяснения - первое название команды, второе название - объяснение, пример использования команды с аргументами/без**\n\n\n**Для участников:**\n\n`crime`, `ограбить` - Ограбить пользователя, `ограбить <упоминание пользователя>`\n\n`Bridge`, `мост` - Стеклянный мост из игры в кальмара, `мост <ставка>`\n\n`Shop`, `магазин` - Магазин ролей, `shop`\n\n`Buy`, `купить` - Купить роль из магазина ролей, `buy <номер роли для покупки>`\n\n`Work`, `работать` - Заработайте немного денег! (Радиус зарплаты определяют администраторы), `work`\n\n`+rep` - Добавить одно очко репутации какому-либо пользователю (Раз в 12 часов), `+rep <упоминание пользователя>`\n\n`-rep` - Убрать одно очко репутации какому-либо пользователю (Раз в 12 часов), `-rep <упоминание пользователя>`\n\n`rep` - Посмотреть репутацию у какого-либо пользователя, `rep <упоминание пользователя>`\n\n`Передать`, `transfer` - Передать деньги какому-либо пользователю, `передать <упоминание пользователя> <сумма для передачи>`\n\n`Аккаунт`, `профиль` - Посмотреть информацию о конкретном пользователе на сервере (или о себе, оставив аргумент пустым), `аккаунт <упоминание пользователя>`\n\n`Лидеры`, `leaderboard` - Доска лидеров по балансу (Топ 10), `лидеры`\n\n`переводб`, `transferb` - Перевод со своего банковского счета, на другой (при условии наличия банкомата в канале), `переводб <упоминание пользователя> <сумма перевода>`\n\n`Положить`, `dep` - Положить деньги на свой банковский счет (при условии наличия банкомата в канале), `положить <сумма пополнения>`\n\n`Снять`, `grab` - Снять деньги со своего банковского счета, `снять <сумма снятия>`\n\n`Казино`, `casino` - Сыграйте в казино (правила указаны в команде), `казино <сумма>`\n\n\n**Для администрации:**\n\n`Зарплата`, `set_work` - Указать радиус зарплаты, `зарплата <минимальное зарплата> <максимальная зарплата>`\n\n`add_role`, `add_shop` - Добавить роль в магазин, `add_role <упоминание роли> <цена>`\n\n`remove_role`, `remove_shop` - Удалить роль из магазина, `remove_role <упоминание роли>`\n\n`Добавить`, `add` - Добавить денег на счет пользователя, `add <упоминание пользователя> <сумма начисления> <банк/наличные>`\n\n`Удалить`, `remove` - Удалить деньги со счета, `remove <упоминание пользователя> <сумма для удаления или all> <банк/наличные>`\n\n`+банк`, `addatm` - Добавить в канал банкомат, `+банк <упоминание канала (необязательно)>`\n\n`-банк`, `rematm` - Убрать из канала банкомат, `-банк <упоминание канала(необязательно)>`\n\n`+казино`, `addcasino` - Добавить в канал казино, `+казино <упоминание канала(необязательно)>`\n\n`-казино`, `remcasino` - Удалить из канала казино, `-казино <упоминание канала(необязательно)>`",
                                  color=0x7300ff)

            embed.set_author(name="heckerBOT", url="https://discord.gg/PvRHYF4djp",
                             icon_url="https://cdn.discordapp.com/avatars/944890163975323728/e795126f4bed13c0348ae3dd69cc44d4.png?size=1024")

            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.label == '5':
            embed = disnake.Embed(title="**МЕЖСЕРВЕРНЫЙ ЧАТ**",
                                  description="**Внимание! Перед командой ставьте звездочку!\nФормат объяснения - первое название команды, второе название - объяснение, пример использования команды с аргументами/без**\n\n`Чат`, `chat` - Посмотреть настройки чата, `чат`\n\n`Чат_а`, `chat_a` - Включение/выключение межсерверного чата, установка канала для межсерверного чата, `чат_а <переключить/канал> <упоминание канала (если предыдущее условие канал)>`\n\n`Чат_серв`, `chat_serv` - Просмотр доступных серверов, сопряжение с сервером, распряжение с сервером, бан/разбан участников с другого сервера по айди (не бан а МУТ), банлист учатников, бан/разбан серверов (что-бы не могли сопряжатся с вами), банлист серверов, `чат_серв <добавить/удалить/бан/разбан/банлист/бан-с/разбан-с/банлист-с> <айди участника или сервера>`\n\n`Уровень`, `lvl` - Информация о вашем уровне, опыте, арбузах и бутербродах, `lvl <упоминание пользователя(необязательно)>`\n\n`Уровень_а`, `lvl_a` - Включение/выключение подарков между серверами, указание цены бутербродам и арбузам, узнать информацию об этом, `уровень_а <бутерброд, арбуз, подарки или оставьте пустым для информации> <цена для арбуза или бутерброда>`\n\n`Обмен`, `swap` - Обменять арбузы/бутерброды на наличные деньги, `обмен <бутерброд/арбуз> <кол-во>`\n\n`Подарить`, `gift` - Подарить бутерброды/арбузы пользователю на другом сервере, `подарить <айди пользователя> <арбуз/бутерброд> <кол-во>`\n\nПример настройки межсерверного чата - \n1. `*чат_а переключить` - Включаем межсерверный чат\n2. `*чат_а канал <упоминание канала>` - Устанавливаем канал для чата\n3. `*чат_серв` - Просматриваем доступные сервера для подключения\n 4. `*чат_серв добавить <id сервера для подключения>` - Подключаемся к серверу",
                                  color=0x7300ff)

            embed.set_author(name="heckerBOT", url="https://discord.gg/PvRHYF4djp",
                             icon_url="https://cdn.discordapp.com/avatars/944890163975323728/e795126f4bed13c0348ae3dd69cc44d4.png?size=1024")

            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.label == '6':
            with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
                with db.cursor() as c:
                    c.execute(f"SELECT id FROM premium WHERE id = {interaction.user.id}")
                    if c.fetchone() is None:
                        if interaction.guild is None:
                            await interaction.response.send_message("Этот раздел доступен только на сервере!")
                            return
                        if interaction.user.guild_permissions.administrator is False:

                            await interaction.response.send_message("У вас нет премиума или прав администратора! Кстати, премиум можно приобрести на [boosty](https://boosty.to/heckerbot) или переводом мне на киви, присутствие на сервере поддержки ОБЯЗАТЕЛЬНО для покупки премиума. ", ephemeral=True)
                            return
                        else:
                            pass


                    embed = disnake.Embed(title="**ПРЕМИУМ**",
                                        description="**Внимание! Перед командой ставьте звездочку!\n\nФормат объяснения - первое название команды, второе название - объяснение, пример использования команды с аргументами/без**\n\n`ip` - Пробив по айпи, `ip <ip адрес или доменное имя>`\n`sudo` - Главное условие почти для всех команд премиума, `sudo <аргументы>`\n`sudo apt` - информация о командах apt, а также сами команды apt, `sudo apt <install/remove> <heck>`\n`sudo heck` - Команды взлома (сейчас доступно только две - heck jopa и heck meteor), `sudo heck <jopa/pentagon/life/meteor/оставить пустым для инфы>`\n\nКстати, если вас задолбали эти взломы, то вы можете обратиться на сервер поддержки для отключения команд взлома на вашем сервере. (Для админа/создателя сервера)",
                                        color=0x7300ff)

                    embed.set_author(name="heckerBOT", url="https://discord.gg/PvRHYF4djp",
                                    icon_url="https://cdn.discordapp.com/avatars/944890163975323728/e795126f4bed13c0348ae3dd69cc44d4.png?size=1024")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                
            


class MyCustomView(disnake.ui.View):
    message: disnake.Message
    
    def __init__(self, ctx, message_id: int):
        super().__init__(timeout=90)
        self.ctx = ctx
        self.message_id = message_id
        self.add_item(BButton(style=disnake.ButtonStyle.green,
                              label="1",
                              custom_id="1" + str(self.message_id)))
        self.add_item(BButton(style=disnake.ButtonStyle.green,
                              label="2",
                              custom_id="2" + str(self.message_id)))
        self.add_item(BButton(style=disnake.ButtonStyle.green,
                              label="3",
                              custom_id="3" + str(self.message_id)))
        self.add_item(BButton(style=disnake.ButtonStyle.green,
                              label="4",
                              custom_id="4" + str(self.message_id)))
        self.add_item(BButton(style=disnake.ButtonStyle.green,
                              label="5",
                              custom_id="5" + str(self.message_id)))
        self.add_item(BButton(style=disnake.ButtonStyle.red,
                              label="6",
                              custom_id="6" + str(self.message_id)))

    async def on_timeout(self):
        # кнопочки больше не будут работать
        # Once the view times out we disable the first button and remove the second button
        self.children[0].disabled = True  # type: ignore
        self.children[1].disabled = True  # type: ignore
        self.children[2].disabled = True  # type: ignore
        self.children[3].disabled = True  # type: ignore
        self.children[4].disabled = True  # type: ignore
        self.children[5].disabled = True  # type: ignore

        # make sure to update the message with the new buttons
        try:
            await self.message.edit(view=self)
        except:
            pass
        self.stop()



class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_command_error(self, inter, error):
        send_help = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError, commands.NoPrivateMessage)
        try:
            print(f'{error} - {inter.guild.name} - {inter.message.author.name}')
        except:
            pass

        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title="<:onno:954815596082659368>Отказ<:onno:954815596082659368>",
                                  description=f"<@!{inter.message.author.id}> \nУ тебя (или меня) нет прав для выполнения этой команды.<:onno:954815596082659368>\nПодробная ошибка: {error}",
                                  color=0xff0000)
            await inter.channel.send(embed=embed)
            return
        elif isinstance(error, commands.CommandOnCooldown):
            embed = disnake.Embed(
                title='<:onno:954815596082659368>Команда на задержке<:onno:954815596082659368>',
                description=f'Повторить через {math.ceil(error.retry_after)} секунд',
                color=disnake.Color.red())
            member = inter.author
            await member.send(embed=embed)
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, send_help):
            embed = disnake.Embed(title="Ошибка",
                                  description=f"**Произошла ошибка**\n\nВозможные проблемы: вы неправильно указали условия команды, вы их не указазали, или команда не может быть выполнена в ЛС.\nПодробная ошибка: {error}",
                                  color=0xff0000)
            await inter.channel.send(embed=embed)
            return
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.CommandError):
            embed = disnake.Embed(title="<:onno:954815596082659368>Извините<:onno:954815596082659368>",
                                  description=f"**Произошла ошибка**\n\nВозможные проблемы: бот не имеет права на выполнение команды, допущена ошибка в коде или вы неправильно указали условия команды.\nПодробная ошибка: {error}",
                                  color=0xff0000)

            await inter.channel.send(embed=embed)
        else:

            await inter.channel.send(error)


    @commands.Cog.listener()
    async def on_user_command_error(self, inter, error):
        send_help = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError, commands.NoPrivateMessage)
        try:
            print(f'{error} - {inter.guild.name} - {inter.message.author.name}')
        except:
            pass

        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title="<:onno:954815596082659368>Отказ<:onno:954815596082659368>",
                                  description=f"<@!{inter.message.author.id}> \nУ тебя (или меня) нет прав для выполнения этой команды.<:onno:954815596082659368>\nПодробная ошибка: {error}",
                                  color=0xff0000)
            try:
                await inter.response.send_message(embed=embed)
            except:
                await inter.followup.send(embed=embed)
            return
        elif isinstance(error, commands.CommandOnCooldown):
            ty_res = time.gmtime(math.ceil(error.retry_after))
            res = time.strftime("%H ч,%M мин,%S сек",ty_res)
            embed = disnake.Embed(
                title='<:onno:954815596082659368>Команда на задержке<:onno:954815596082659368>',
                description=f'Повторить через {res}',
                color=disnake.Color.red())
            try:
                await inter.response.send_message(embed=embed)
            except:
                await inter.followup.send(embed=embed)
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, send_help):
            embed = disnake.Embed(title="Ошибка",
                                  description=f"**Произошла ошибка**\n\nВозможные проблемы: вы неправильно указали условия команды, вы их не указазали, или команда не может быть выполнена в ЛС.\nПодробная ошибка: {error}",
                                  color=0xff0000)
            try:
                await inter.response.send_message(embed=embed)
            except:
                await inter.followup.send(embed=embed)
            return
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.CommandError):
            embed = disnake.Embed(title="<:onno:954815596082659368>Извините<:onno:954815596082659368>",
                                  description=f"**Произошла ошибка**\n\nВозможные проблемы: бот не имеет права на выполнение команды, допущена ошибка в коде или вы неправильно указали условия команды.\nПодробная ошибка: {error}",
                                  color=0xff0000)
            try:
                await inter.response.send_message(embed=embed)
            except:
                await inter.followup.send(embed=embed)
            return
        else:
            try:
                await inter.response.send_message(error)
            except:
                await inter.followup.send(error)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        send_help = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError, commands.NoPrivateMessage)
        try:
            print(f'{error} - {inter.guild.name} - {inter.message.author.name}')
        except:
            pass

        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title="<:onno:954815596082659368>Отказ<:onno:954815596082659368>",
                                  description=f"<@!{inter.message.author.id}> \nУ тебя нет прав для выполнения этой команды.<:onno:954815596082659368>\nПодробная ошибка: {error}",
                                  color=0xff0000)
            await inter.send(embed=embed)
            return
        if isinstance(error, commands.BotMissingPermissions):
            embed = disnake.Embed(title="<:onno:954815596082659368>Блин<:onno:954815596082659368>",
                                  description=f"<@!{inter.message.author.id}> \nУ меня не хватает прав для выполнения данной команды!\nПодробная ошибка: {error}",
                                  color=0xff0000)
            await inter.send(embed=embed)
            return
        
        elif isinstance(error, commands.CommandOnCooldown):
            ty_res = time.gmtime(math.ceil(error.retry_after))
            res = time.strftime("%H ч, %M мин, %S сек", ty_res)
            embed = disnake.Embed(
                title='<:onno:954815596082659368>Команда на задержке<:onno:954815596082659368>',
                description=f'Повторить через {res}',
                color=disnake.Color.red())

            await inter.channel.send(embed=embed)
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, send_help):
            embed = disnake.Embed(title="Ошибка",
                                  description=f"**Произошла ошибка**\n\nВозможные проблемы: вы неправильно указали условия команды, вы их не указазали, или команда не может быть выполнена в ЛС.\nПодробная ошибка: {error}",
                                  color=0xff0000)
            await inter.channel.send(embed=embed)
            return
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.CommandError):
            embed = disnake.Embed(title="<:onno:954815596082659368>Извините<:onno:954815596082659368>",
                                  description=f"**Произошла ошибка**\n\nВозможные проблемы: бот не имеет права на выполнение команды, допущена ошибка в коде или вы неправильно указали условия команды.\nПодробная ошибка: {error}",
                                  color=0xff0000)
            
            await inter.channel.send(embed=embed)
            return
        else:
            try:
                await inter.response.send_message(error)
            except:
                await inter.followup.send(error)
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        send_help = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError, commands.NoPrivateMessage)
        

        if isinstance(error, commands.CommandNotFound):
            return
        
        try:
            print(f'{error} - {ctx.guild.name} - {ctx.message.author.name}')
        except:
            pass
        if isinstance(error, commands.MissingPermissions):

            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_permissions]

            embed = disnake.Embed(title="<:onno:954815596082659368>Отказ<:onno:954815596082659368>",
                                  description=f"<@!{ctx.message.author.id}> \nУ тебя нет права {human_join(missing)} для выполнения этой команды.<:onno:954815596082659368>\nПодробная ошибка: {error}",
                                  color=0xff0000)
            try:
                await ctx.send(embed=embed)
            except:
                await ctx.author.send("У меня нет прав отправлять сообщения в этом канале!")
            return
        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_permissions]
            embed = disnake.Embed(title="<:onno:954815596082659368>Блин<:onno:954815596082659368>",
                                  description=f"<@!{ctx.message.author.id}> \nУ меня не хватает права {human_join(missing)} для выполнения данной команды!\nПодробная ошибка: {error}",
                                  color=0xff0000)
            try:
                await ctx.send(embed=embed)
            except:
                await ctx.author.send("У меня нет прав отправлять сообщения в этом канале!")
            return
        
        
        elif isinstance(error, commands.CommandOnCooldown):

            ty_res = time.gmtime(math.ceil(error.retry_after))
            res = time.strftime("%H ч, %M мин, %S сек", ty_res)
            embed = disnake.Embed(
                title='<:onno:954815596082659368>Команда на задержке<:onno:954815596082659368>',
                description=f'Повторить через {res}',
                color=disnake.Color.red())
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, send_help):
            embed = disnake.Embed(title="Ошибка",
                                  description=f"**Произошла ошибка**\n\nВозможные проблемы: вы неправильно указали условия команды, вы их не указазали, или команда не может быть выполнена в ЛС.\nПодробная ошибка: {error}",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        elif "TimeoutError" in str(error):
            embed = disnake.Embed(title="<:onno:954815596082659368>Извините<:onno:954815596082659368>",
                                  description=f"*Время ожидания вышло.*",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return

        elif isinstance(error, commands.CommandError):

            embed = disnake.Embed(title="<:onno:954815596082659368>Извините<:onno:954815596082659368>",
                                  description=f"**Произошла ошибка**\n\nВозможные проблемы: бот не имеет права на выполнение команды, допущена ошибка в коде или вы неправильно указали условия команды.\nПодробная ошибка: {error}",
                                  color=0xff0000)
            try:
                await ctx.send(embed=embed)
            except:
                await ctx.author.send("У меня нет прав отправлять сообщения в этом канале!")
            return
        
        else:
            await ctx.send(error)

    

            

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = psycopg2.connect(host=host, user=userr, password=password, database=db_name)
        c = db.cursor()

        c.execute(f"SELECT userid, serverid FROM users WHERE userid = {member.id} AND serverid = {member.guild.id}")
        

        if c.fetchone() is not None:
            del_fr_us(member.id, member.guild.id)
            console.log(f"[bold][red]Из БД удалён участник [/red]{member.name} [red]-[/red] {member.guild.name}")
        else:
            pass
        c.close()
        db.close()

        if member.guild.id == 1028282701599477821:
            chnl = self.bot.get_channel(1032358107373895751)
            embed = None
            async for entry in member.guild.audit_logs(limit=2, action=disnake.AuditLogAction.kick):
                if entry.target.id == member.id:

                    embed = disnake.Embed(title="**КИК**",
                                        description=f"{member.mention}({member.name}#{member.discriminator}) Был кикнут админом {entry.user.mention}!",
                                        color=0xff0000)
            if embed is not None:

                await chnl.send(embed=embed)
        if member.guild.id == 844649033502818314:
            chnl = self.bot.get_channel(844942954800087101)
            embed = None
            async for entry in member.guild.audit_logs(limit=2, action=disnake.AuditLogAction.kick):
                if entry.target.id == member.id:

                    embed = disnake.Embed(title="**КИК**",
                                        description=f"{member.mention}({member.name}#{member.discriminator}) Был кикнут админом {entry.user.mention}!",
                                        color=0xff0000)
            if embed is not None:

                await chnl.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        db = psycopg2.connect(host=host, user=userr, password=password, database=db_name)
        c = db.cursor()
        c.execute(f"SELECT userid, serverid FROM users WHERE userid = {member.id} AND serverid = {guild.id}")

        if c.fetchone() is not None:
            del_fr_us(member.id, member.guild.id)
            console.log(f"[bold][red]Из БД удалён участник (забанен) [/red]{member} [red]-[/red] {guild.name}")
            db.commit()
        else:
            pass
        c.close()
        db.close()
        if guild.id == 1028282701599477821:
            chnl = self.bot.get_channel(1032358107373895751)
            async for entry in guild.audit_logs(limit=2, action=disnake.AuditLogAction.ban):
                if entry.target.id == member.id:

                    embed = disnake.Embed(title="**БАН**",
                                        description=f"{member.mention}({member.name}#{member.discriminator}) Был забанен админом {entry.user.mention}!",
                                        color=0xff0000)
            await chnl.send(embed=embed)
        if guild.id == 844649033502818314:
            chnl = self.bot.get_channel(844942954800087101)
            async for entry in guild.audit_logs(limit=2, action=disnake.AuditLogAction.ban):
                if entry.target.id == member.id:

                    embed = disnake.Embed(title="**БАН**",
                                        description=f"{member.mention}({member.name}#{member.discriminator}) Был забанен админом {entry.user.mention}!",
                                        color=0xff0000)
            await chnl.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        if guild.id == 1028282701599477821:
            chnl = self.bot.get_channel(1032358107373895751)
            async for entry in guild.audit_logs(limit=2, action=disnake.AuditLogAction.unban):
                if entry.target.id == member.id:

                    embed = disnake.Embed(title="**РАЗБАН**",
                                description=f"{member.mention}({member.name}#{member.discriminator}) Был разбанен админом {entry.user.mention}!",
                                color=0xff0000)
            await chnl.send(embed=embed)
        if guild.id == 844649033502818314:
            chnl = self.bot.get_channel(844942954800087101)
            async for entry in guild.audit_logs(limit=2, action=disnake.AuditLogAction.unban):
                if entry.target.id == member.id:

                    embed = disnake.Embed(title="**РАЗБАН**",
                                description=f"{member.mention}({member.name}#{member.discriminator}) Был разбанен админом {entry.user.mention}!",
                                color=0xff0000)
            await chnl.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.current_timeout is None:
            if after.current_timeout is not None:
                if after.guild.id == 1028282701599477821:
                    chnl = self.bot.get_channel(1032358107373895751)
                    async for entry in after.guild.audit_logs(limit=2, action=disnake.AuditLogAction.member_update):
                        if entry.target.id == after.id:


                    
                        
                            embed = disnake.Embed(title="**МУТ**",
                                        description=f"{after.mention}({after.name}#{after.discriminator}) Будет(Был) размучен <t:{round(after.current_timeout.timestamp())}:R>!\nАдмин - {entry.user.mention}",
                                        color=0xff0000)
                    await chnl.send(embed=embed)
                if after.guild.id == 844649033502818314:
                    chnl = self.bot.get_channel(844942954800087101)
                    async for entry in after.guild.audit_logs(limit=2, action=disnake.AuditLogAction.member_update):
                        if entry.target.id == after.id:


                    
                        
                            embed = disnake.Embed(title="**МУТ**",
                                        description=f"{after.mention}({after.name}#{after.discriminator}) Будет(Был) размучен <t:{round(after.current_timeout.timestamp())}:R>!\nАдмин - {entry.user.mention}",
                                        color=0xff0000)
                    await chnl.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 844649033502818314:
            chnl = self.bot.get_channel(844656520095465524)
            chnl2 = self.bot.get_channel(844656219213004891)
            await chnl.send(f"{member.mention}, привет, шуруй в {chnl2.mention}")
        if not member.bot:
            db = psycopg2.connect(host=host, user=userr, password=password, database=db_name)
            c = db.cursor()


            c.execute(f"SELECT userid, serverid FROM users WHERE userid = {member.id} AND serverid = {member.guild.id}")
            if c.fetchone() is None:

                c.execute(f"INSERT INTO users (userid, serverid, nickname, mention, balance, bank, rep, counter, lvl, sandw, waterm, lastmes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (member.id, member.guild.id, member.name, f'<@!{member.id}>', 0, 0, 0, 0, 0, 0, 0, None))  # вводит все данные об участнике в БД

                console.log(f"[bold][green]В БД добавлен участник [/green]{member} [green]-[/green] {member.guild.name}")
                db.commit()
            else:
                pass
            c.close()
            db.close()

    


    



    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1046162165205315665:
            await message.add_reaction("<:bsyes:1049954302740938802>")
            await message.add_reaction("<:bsno:1049954315365789696>")
        if message.content.startswith("*"):
            return
        if message.author.bot:
            return
        if message.guild is None:
            return
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                c.execute(f"SELECT id FROM ban WHERE id = {message.author.id}")
                if c.fetchone() is not None:
                    return
                c.execute(f"SELECT enabled FROM guild WHERE serverid = {message.guild.id}")
                try:
                    if c.fetchone()[0] == "Disabled":
                        return
                except Exception:
                    print(message.author.name)
                    console.print_exception(show_locals=True)
                c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {message.guild.id}")
                if c.fetchone()[0] == 0:
                    return
                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {message.guild.id}")
                if c.fetchone()[0] is None:
                    return
                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {message.guild.id}")
                if message.channel.id != c.fetchone()[0]:
                    return


                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {message.guild.id}")
                chnl = self.bot.get_channel(c.fetchone()[0])

                c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {message.guild.id}")
                guildtu = self.bot.get_guild(c.fetchone()[0])
                
                c.execute(f"SELECT enabled FROM guild WHERE serverid = {guildtu.id}")
                if c.fetchone()[0] == "Disabled":
                    await chnl.send("У этого сервера отключен чат!")
                    return
                c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {guildtu.id}")
                if c.fetchone()[0] == 0:
                    await chnl.send("У этого сервера вы не указаны как сопряженный сервер? Идите на сервер поддержки")
                    return
                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {guildtu.id}")
                if c.fetchone()[0] is None:
                    await chnl.send("У этого сервера не указан межсерверный канал!")
                    return
                c.execute(f"SELECT chnlid FROM guild WHERE serverid = {guildtu.id}")
                chnltu = self.bot.get_channel(c.fetchone()[0])
                if chnltu is None:
                    await message.channel.send("У этого того проблема с каналом!")
                    await guildtu.owner.send("Здравствуйте! Бот столкнулся с проблемой, он не видит канала для межсерверного чата (к вам написали сообщение)")
                    c.execute("UPDATE guild SET chnlid = %s WHERE serverid = %s AND enabled = %s AND serveridtu = %s", (None, guildtu.id, 'Enabled', 0))
                    db.commit()



                c.execute(f"SELECT serverid FROM banned WHERE serverid = {guildtu.id} AND memberid = {message.author.id}")

                if c.fetchone() is not None:
                    await message.author.send("Вы забанены для межсерверного чата!")
                    await message.delete()
                    return
                c.execute(f"SELECT lastmes FROM users WHERE serverid = {message.guild.id} AND userid = {message.author.id}")
                lastmes = c.fetchone()
                if lastmes is None:
                    pass
                else:
                    if lastmes[0] == message.content:
                        await message.delete()
                        return
                try:
                    c.execute(f"UPDATE users SET lastmes = '{message.content}' WHERE serverid = {message.guild.id} AND userid = {message.author.id}")
                    db.commit()
                except:
                    c.execute("ROLLBACK")
                    db.commit()


                embedd = disnake.Embed(title="** **",
                                    description=message.content,
                                    color=0x5900ff,
                                    timestamp=message.created_at)
                embedd.set_author(name=f'{message.author.name} - {message.author.id} - {message.guild.name}')
                
                if message.author.avatar is not None:
                    embedd.set_author(name=f'{message.author.name} - {message.author.id} - {message.guild.name}', icon_url=message.author.avatar.url)
                else:
                    embedd.set_author(name=f'{message.author.name} - {message.author.id} - {message.guild.name}')
                try:
                    await chnltu.send(embed=embedd)
                except:
                    c.execute(f"SELECT serverid FROM banned WHERE serverid = {message.guild.id}")
                    if c.fetchone() is not None:
                        c.execute(f"DELETE FROM banned WHERE serverid = {message.guild.id}")


                    c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {message.guild.id}")
                    c.execute(f"SELECT serverid FROM banned WHERE serverid = {c.fetchone()[0]}")
                    if c.fetchone() is not None:
                        c.execute(f"SELECT serveridtu FROM guild WHERE serverid = {message.guild.id}")
                        c.execute(f"DELETE FROM banned WHERE serverid = {c.fetchone()[0]}")
                    c.execute(f"UPDATE guild SET serveridtu = 0 WHERE serverid = {message.guild.id}")
                    c.execute(f"UPDATE guild SET serveridtu = 0 WHERE serveridtu = {message.guild.id}")
                    db.commit()
                    await message.channel.send("Сервер экстренно отсоединен, бот не может отправить сообщение на другой сервер")
                    return
                await message.add_reaction("<a:yees:952255158992142417>")
                a = len(message.content.split())
                words = int(a)
                if words > 25:
                    return
                # for zero lvl
                if words == 0:
                    return
                if words < 2:
                    return


                c.execute(f"SELECT lvl FROM users WHERE serverid = {message.guild.id} AND userid = {message.author.id}")
                lvl = c.fetchone()[0]
                if lvl == 0:
                    maxcount = 50
                    c.execute(f"SELECT counter FROM users WHERE serverid = {message.guild.id} AND userid = {message.author.id}")
                    counterdo = c.fetchone()[0]
                    
                    c.execute(f"UPDATE users SET counter = counter + {words} WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                    db.commit()
                    c.execute(f"SELECT counter FROM users WHERE serverid = {message.guild.id} AND userid = {message.author.id}")
                    counter = c.fetchone()[0]
                    polovina = maxcount / 2
                    if counterdo < polovina:
                        if counter > polovina:
                            c.execute(f"UPDATE users SET sandw = sandw + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                            db.commit()
                            await message.author.send("Вы получили один бутерброд за общение!")



                    if counter > maxcount:
                        ostatok: int = counter - maxcount
                        c.execute(f"UPDATE users SET counter = 0 + {ostatok} WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        c.execute(f"UPDATE users SET lvl = lvl + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        c.execute(f"UPDATE users SET waterm = waterm + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        db.commit()
                        await message.author.send("Вы получили новый уровень! (И один арбуз)")
                        return
                    elif counter == maxcount:
                        c.execute(f"UPDATE users SET counter = 0 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        c.execute(f"UPDATE users SET lvl = lvl + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        c.execute(f"UPDATE users SET waterm = waterm + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        db.commit()
                        await message.author.send("Вы получили новый уровень! (И один арбуз)")
                        return
                    else:
                        c.execute(f"UPDATE users SET counter = counter + {words} WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        db.commit()
                else:
                    maxcount = 50*lvl
                    c.execute(f"SELECT counter FROM users WHERE serverid = {message.guild.id} AND userid = {message.author.id}")
                    counterdo = c.fetchone()[0]
                    
                    c.execute(f"UPDATE users SET counter = counter + {words} WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                    db.commit()
                    c.execute(f"SELECT counter FROM users WHERE serverid = {message.guild.id} AND userid = {message.author.id}")
                    counter = c.fetchone()[0]
                    polovina = maxcount / 2
                    if counterdo < polovina:
                        if counter > polovina:
                            c.execute(f"UPDATE users SET sandw = sandw + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                            db.commit()
                            await message.author.send("Вы получили один бутерброд за общение!")



                    if counter > maxcount:
                        ostatok: int = counter - maxcount
                        c.execute(f"UPDATE users SET counter = 0 + {ostatok} WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        c.execute(f"UPDATE users SET lvl = lvl + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        c.execute(f"UPDATE users SET waterm = waterm + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        db.commit()
                        await message.author.send("Вы получили новый уровень! (И один арбуз)")
                        return
                    elif counter == maxcount:
                        c.execute(f"UPDATE users SET counter = 0 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        c.execute(f"UPDATE users SET lvl = lvl + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        c.execute(f"UPDATE users SET waterm = waterm + 1 WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        db.commit()
                        await message.author.send("Вы получили новый уровень! (И один арбуз)")
                        return
                    else:
                        c.execute(f"UPDATE users SET counter = counter + {words} WHERE userid = {message.author.id} AND serverid = {message.guild.id}")
                        db.commit()


            















    



    @commands.command(aliases=['помощь', 'help'])
    @pidor()
    async def __help(self, ctx):
        view = MyCustomView(ctx=ctx, message_id=ctx.message.id)

        embed = disnake.Embed(title="**ПОМОЩЬ**",
                              description="\n*помощь\n\nВот список категорий:\n\n1. **Модерирование**\n\n2. **Утилиты**\n\n3. **Вещи сделанные просто так и не имеющие смысла**\n\n4. **Экономика и всё сопутствующее**\n\n5. **Межсерверный чат**\n\n6. **ПРЕМИУМ**  \n\n\nПочти каждый день я добавляю новые команды! Заглядывайте иногда.\n\nP.S - Кнопочки работают не вечно.",
                              color=0x7300ff)
        embed.set_author(name="heckerBOT", url="https://discord.gg/PvRHYF4djp",
                         icon_url="https://cdn.discordapp.com/avatars/944890163975323728/e795126f4bed13c0348ae3dd69cc44d4.png?size=1024")

        view.message = await ctx.send(embed=embed, view=view)




    @commands.command()
    async def s(self, ctx, *, text):
        if ctx.message.author.id not in bid:
            await ctx.send("Данную команду может выполнить только команда создателя бота!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)
            return
        print(text)
        await ctx.send(text)
        await ctx.message.delete()

    @commands.command()
    async def rl(self, ctx):
        if ctx.message.author.id not in bid:
            await ctx.send("Данную команду может выполнить только команда создателя бота!")
            return
        embed = disnake.Embed(title="ПРАВИЛА",
                              description="**ЗАПРЕЩЕНО**\n\n 1.1 Запрещено не использовать ненормативную лексику)(Россия, хули) \n1.2 Писать бессмысленную или малосодержательную информацию, не несущую смысловой нагрузки (флудить-спамить). \n1.3 Флудить смайликами. (Эмодзи) \n1.4 Оскорблять людей (провоцировать, троллить, угрожать, клеветать)(Если человек не в обиде, можно) \n1.5 Пропаганда вредных привычек, нацизма, расизма, сексизма, суицида и прочее. \n1.6. Запускать скримеры в голосовых чатах. \n1.7 Любое проявление рекламы (Ссылка на свой аккаунт/профиль/деятельность) с просьбой подписаться, или извлечь из этого выгоду. \n1.8 Обсуждение действий администрации \n1.9 Обсуждать политические темы. \n2.0 Выдача себя за другую личность этого сервера. \n2.1 Деанон любого участника без его согласия (раскрытие настоящего ФИО члена сервера, фото, город проживания, работа и т.д.) \n\nНезнание правил не освобождает от ответственности. Не пытайтесь найти недостатки в правилах сервера, если это не прописано в правилах, это не значит что так можно делать. Также администрация не имеет права нарушать данный свод правил. Данное сообщение может быть изменено без оповещения.\n||@everyone||",
                              color=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(aliases=['servers', 'сервера'])
    async def __servers(self, ctx):
        if ctx.message.author.id not in bid:
            await ctx.send("Данную команду может выполнить только команда создателя бота!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)
            return
        e = ' \n '.join([str(server) for server in self.bot.guilds])
        y = len(self.bot.guilds)

        embed = disnake.Embed(title="Сейчас активен на " + str(y) + " серверах:",
                              description=e, color=0x5e0da0)
        return await ctx.send(embed=embed)

    @commands.command(description="1000 - 7")
    async def ghoul(self, ctx):
        if ctx.message.author.id not in bid:
            await ctx.send("Данную команду может выполнить только команда создателя бота!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)
            return
        await ctx.send("Я умер прости")
        x = 1007 - 7

        while x > 7:
            ra = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            res = random.choice(ra)
            await ctx.send(f"{x} - 7 = {x - 7}")
            x -= 7
            await asyncio.sleep(1)
            if res == 5:
                ph = ["https://media.tenor.com/images/06569902c0030a33dc01810b2c427658/tenor.gif",
                      "https://media.tenor.com/images/4f14f7da5796ccd3c5a01325b696fa0b/tenor.gif",
                      "https://media.tenor.com/images/89844d4edc2c63d86c2232bb7398c389/tenor.gif",
                      "https://media.tenor.com/images/526ae02effb10de4201cc8b23f21ed86/tenor.gif",
                      "https://media.tenor.com/images/ce8e5975b25290346e127e3b8c84b945/tenor.gif"]
                await ctx.send(random.choice(ph))
        await ctx.send('Я гуль')
        await ctx.send("https://media.tenor.com/images/d1e21bf1d296d572d47f7d8fc7abfdfa/tenor.gif")

    @commands.command()
    async def gay(self, ctx, message: disnake.Member):
        if ctx.message.author.id not in bid:
            await ctx.send("Данную команду может выполнить только команда создателя бота!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)
            return
        if message == "_Максус_208_":
            await ctx.send("Он не гей! Ты охуел?")
            return
        if message == "<@!860932389836685313>":
            await ctx.send("Он не гей! Ты охуел?")
            return
        if message == "heckerBOT":
            await ctx.send("Я не гей! Ты охуел?")
            return
        if message == "heckerBOT":
            await ctx.send("Я не гей! Ты охуел?")
            return
        if message == "<@950408761401557035":
            await ctx.send("Я не гей! Ты охуел?")
            return
        if message == "<@944890163975323728>":
            await ctx.send("Я не гей! Ты охуел?")
            return
        if message == "Хэкер":
            await ctx.send("Сам ты гей блять, он святой.")
            return
        if message == "хэкер":
            await ctx.send("Сам ты гей блять, он святой.")
            return
        if message == "<@!388298424027709440>":
            await ctx.send("Сам ты гей блять, он святой.")
            return

        await ctx.send(f"Внимание, {message.mention}, превращаю вас в гея!")
        x = 0
        while x <= 99:
            await ctx.send(f"{x + 1}%")
            x += 1
            await asyncio.sleep(1)
        await ctx.send(f'{message.mention}, теперь ты гей!')
    @commands.command()
    async def sql(self, ctx, *, a):
        if ctx.message.author.id not in bid:
            return
        
        with closing(psycopg2.connect(host=host, user=userr, password=password, database=db_name)) as db:
            with db.cursor() as c:
                try:
                    c.execute(a)
                    db.commit()
                    await ctx.send("Готово!")
                except Exception:
                    c.execute('ROLLBACK')
                    db.commit()
                    await ctx.send(Exception)

    @commands.command()
    async def tt(self, ctx, *, member: disnake.Member):
        if ctx.message.author.id not in bid:
            return
        await member.send(f"Внимание, @{member}, превращаю вас в гея!")
        x = 0
        print(f"{member}")
        while x <= 99:
            await member.send(f"{x + 1}%")
            x += 1
            await asyncio.sleep(1)
        print(f"{member}")
        await member.send(f'@{member}, теперь ты гей!')

    @commands.command(aliases=['покинуть', 'leave'])
    async def __leave(self, ctx, guild_id):
        if ctx.message.author.id not in bid:
            return
        await ctx.send("Я дед инсайд")
        await asyncio.sleep(2)
        await ctx.send("Пока")
        await self.bot.get_guild(int(guild_id)).leave()

    @commands.command()
    async def how(self, ctx):
        if ctx.message.author.id not in bid:
            await ctx.send("Данную команду может выполнить только команда создателя бота!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)
            return
        embed = disnake.Embed(  # title="** *ТЫК* **",
            # description='Кто это читает - большой молодец! Спасибо что добавили моего бота на свой сервер!\n\n\nЕсли что, список команд доступен по " * помощь < номер > "',
            color=0x5900ff)
        embed.set_author(name="ТЫК", url="https://dsc.gg/vanger",
                         icon_url="https://cdn.discordapp.com/avatars/944890163975323728/e795126f4bed13c0348ae3dd69cc44d4.png?size=1024")
        await ctx.send(embed=embed)

    @commands.command()
    async def helpme(self, ctx):
        if ctx.message.author.id not in bid:
            await ctx.send("Данную команду может выполнить только команда создателя бота!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)
            return
        await ctx.send(f"Привет, <@!{ctx.message.author.id}>. Опять тебя 'превратили' в гея или еще чего похуже?")
        await asyncio.sleep(2.3)
        await ctx.send(f"Сейчас я все исправлю!")
        x = 0
        while x <= 99:
            await ctx.send(f"{x + 1}%")
            x += 1
            await asyncio.sleep(1)
        await ctx.send(f"Поздравляю!")
        await asyncio.sleep(2)
        await ctx.send(f"Ты снова абсолютно нормальный человек!")



def setup(bot):
    bot.add_cog(user(bot))
