import asyncio
from contextlib import closing
import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions, bot_has_permissions
import psycopg2
from main import bot
import datetime
import aiohttp
from time import perf_counter

from config import password, host, db_name, token, bid
from config import user as userr
from rich.console import Console
from time import sleep
from rich.markdown import Markdown
console = Console()

bot.session = aiohttp.ClientSession()

async def timeout_user(*, user_id: int, guild_id: int, until, sbot):
    headers = {"Authorization": f"Bot {sbot.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}
    print(json)
    async with bot.session.patch(url, json=json, headers=headers) as session:
        print(session)
        if session.status in range(200, 299):
           return True
        return False
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

class moderate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    
        

    @commands.command()
    @commands.guild_only()
    async def q(self, ctx):
        print('a')
        print(self.bot.get_guild(1039231474873929738).owner.name)
        print(self.bot.get_guild(1039231474873929738).owner.discriminator)

    @commands.command(aliases=['очистить', 'clean', 'clear'])
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    @pidor()
    @commands.guild_only()
    async def __clear(self, ctx, amount=5):
        amount += 1
        await ctx.channel.purge(limit=amount)


    @commands.command(aliases=["kick", "кик"])
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @commands.guild_only()
    @pidor()
    async def __kick(self, ctx, member: disnake.Member, *, reason = None):
        if member == ctx.message.guild.owner:
            await ctx.send("Это создатель!")
            return
        if member == ctx.message.author:
            await ctx.send("Вы не можете кикнуть самого себя!")
            return
        if member not in ctx.message.guild.members:
            await ctx.send("Этого пользователя нет?")
            return
        try:
            if reason is None:
                reason = "Причина не указана"
            await member.kick(reason=f"{reason} ({ctx.message.author.name}#{ctx.message.author.discriminator})")
        except:
            await ctx.send("<:onno:954815596082659368>У меня не получилось кикнуть данного пользователя!<:onno:954815596082659368>")
            return


        embed = disnake.Embed(title="Кик",
                      description=f"{ctx.message.author.mention}, кик выполнен успешно!\n\nЦель: {member.mention}\nПричина кика: {reason}\nАдмин/модератор: {ctx.message.author.mention}",
                      color=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(aliases=["mute", "мут"])
    @has_permissions(moderate_members=True)
    @bot_has_permissions(moderate_members=True)
    @pidor()
    async def __timeout(self, ctx, member: disnake.Member, until: int, *, reason = None):
        if reason is None:
            reason = "Причина не указана"

        handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=until, sbot=self.bot)
        if handshake:
            embed = disnake.Embed(title="Мут",
                      description=f"{ctx.message.author.mention}, мут выполнен успешно!\n\nЦель: {member.mention}\nПричина мута: {reason}\nАдмин/модератор: {ctx.message.author.mention}\nВремя мута (в минутах): {until}",
                      color=0xff0000)
            

            return await ctx.send(embed=embed)
        await ctx.send("<:onno:954815596082659368>У меня не получилось замутить данного пользователя!<:onno:954815596082659368>")

    @commands.command(aliases=["ban", "бан"])
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @pidor()
    @commands.guild_only()
    async def __ban(self, ctx, member: disnake.Member, *, reason = None):
        if member == ctx.message.guild.owner:
            await ctx.send("Это создатель!")
            return
        if member == ctx.message.author:
            await ctx.send("Вы не можете забанить самого себя!")
            return
        if member not in ctx.message.guild.members:
            await ctx.send("Этого пользователя нет?")
            return
        try:
            if reason is None:
                reason = "Причина не указана"
            await member.ban(reason=f"{reason} ({ctx.message.author.name}#{ctx.message.author.discriminator})", delete_message_days=0)
        except:
            await ctx.send("<:onno:954815596082659368>У меня не получилось забанить данного пользователя!<:onno:954815596082659368>")
            return


        embed = disnake.Embed(title="Бан",
                      description=f"{ctx.message.author.mention}, бан выполнен успешно!\n\nЦель: {member.mention}\nПричина бана: {reason}\nАдмин/модератор: {ctx.message.author.mention}",
                      color=0xff0000)
        await ctx.send(embed=embed)


        



    @commands.command()
    @has_permissions(manage_roles=True)
    @commands.guild_only()
    @pidor()
    async def разсука(self, ctx, member: disnake.Member = None):
        if ctx.message.guild.id != 951180965097639936:
            return
        guild = self.bot.get_guild(951180965097639936)
        role = guild.get_role(952190066388766760)
        await member.remove_roles(role)
        emoji = '<a:yees:952255158992142417>'
        message = ctx.message
        await message.add_reaction(emoji)

    @commands.command()
    @has_permissions(manage_roles=True)
    @commands.guild_only()
    @pidor()
    async def сука(self, ctx, member: disnake.Member = None):
        if ctx.message.guild.id != 951180965097639936:
            return
        guild = self.bot.get_guild(951180965097639936)
        role = guild.get_role(952190066388766760)
        await member.add_roles(role)
        emoji = '<a:yees:952255158992142417>'
        message = ctx.message
        await message.add_reaction(emoji)



def setup(bot):
    bot.add_cog(moderate(bot))
