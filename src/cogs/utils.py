import discord
from discord.ext import commands

import datetime

from client import logger

class Utils(commands.Cog):
    
    def __init__(self, bot):
        self.bot : commands.Bot = bot

    @commands.command()
    async def lifetime(self, ctx: commands.Context, member: discord.Member):
        """
        Muestra cuanto tiempo lleva siendo miembro en el servidor
        """
        if member.id == self.bot.user.id:
            await ctx.message.add_reaction('🤨')
            return
        
        response: str = ''
        
        def number_to_month_esp(num: int) -> str | None:
            months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            return months[num-1]
        date : datetime.datetime = member.joined_at
        response += f'<@{member.id}> se unio a {ctx.guild.name} el {date.day} de {number_to_month_esp(date.month).lower()} de {date.year}'
        
        def membertime(since: datetime.datetime) -> datetime.timedelta:
            now = datetime.datetime.now(tz=since.tzinfo)
            return now - since
        response += '\n' + f'Lleva siendo miembro del servidor durante '
        time : datetime.timedelta = membertime(date)
        years, days = divmod(time.days,365)
        if years:
            response += f'{years} año' + ('s' if years > 1 else '')
            if days:
                response += f' y {days} dia' + ('s' if days > 1 else '')
        elif days:
            response += f'{days} dia' + ('s' if days > 1 else '')
        else:
            response += 'menos de 24 horas'
        
        await ctx.send(response)
        
async def setup(bot : commands.Bot):
    try:
        cog = Utils(bot)
        await bot.add_cog(cog)
    except Exception as e:
        logger.error(f'Error loading {cog.qualified_name} cog')