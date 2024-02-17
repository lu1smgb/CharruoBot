import discord
from discord.ext import commands

from random import random, randint
from secrets import choice

from client import logger

class Rng(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command()
    async def rng(self, ctx: commands.Context):
        """
        Genera un decimal aleatorio entre 0 y 1
        """
        number = random()
        await ctx.send(f'Ha salido el numero: {number}')
        
    @commands.command()
    async def dado(self, ctx: commands.Context, *args):
        """
        Tira los datos un numero determinado de veces
        
        arg[0]: Numero limite que pueden sacar los dados
        arg[1]: Veces que tiras los dados
        """
        MIN_CARAS = 4
        MAX_CARAS = 100
        MIN_VECES = 1
        MAX_VECES = 10
        
        caras: int = 6
        veces: int = 1
        
        if len(args) >= 1:
            input_caras = int(args[0])
            if input_caras >= MIN_CARAS and input_caras <= MAX_CARAS:
                caras = input_caras
            elif input_caras == 2:
                await ctx.send('❌ Para eso tiro monedas 😕')
                return
            else:
                await ctx.send(f'❌ El numero de *caras* tiene que ser entre {MIN_CARAS} y {MAX_CARAS}')
                return
            
        if len(args) >= 2:
            input_veces = int(args[1])
            if input_veces >= MIN_VECES and input_veces <= MAX_VECES:
                veces = input_veces
            else:
                await ctx.send(f'❌ El numero de *veces* tiene que ser entre {MIN_VECES} y {MAX_VECES}')
                return
        
        await ctx.send('🎲 _Tirando los dados..._ 🎲')
        resultados = [('[' + str(randint(1,caras)) + ']') for _ in range(veces)]
        await ctx.send(', '.join(resultados))
                
    @commands.command()
    async def moneda(self, ctx: commands.Context, *args):
        MIN_VECES = 1
        MAX_VECES = 100
        CARA = '🟢'
        CRUZ = '❌'
        veces = 1
        if len(args) >= 1:
            input_veces = int(args[0])
            if input_veces < MIN_VECES or input_veces > MAX_VECES:
                await ctx.send(f'❌ El numero de veces a tirar la moneda tiene que ser entre {MIN_VECES} y {MAX_VECES}')
                return
            veces = input_veces
        
        await ctx.send(f'_🤜 Tirando {veces} monedas... 🤛_\n')
        
        response = ''
        resultados : list[bool] = [choice([CARA,CRUZ]) for _ in range(veces)]
        for i in range(veces):
            if i % 10 == 0 and i > 0:
                response += '\n'
            response += resultados[i]
        
        if veces > 10:
            response += f'\n\n{CARA} (Cara) = {resultados.count(CARA)}\n'
            response += f'{CRUZ} (Cruz) = {resultados.count(CRUZ)}'
            
        await ctx.send(response)
        
    
    @commands.command()
    async def equipos(self, ctx: commands.Context, *args):
        if ctx.author.voice is None:
            await ctx.send('❌ Debes estar en un canal de voz para poder usar este comando')
            return
        
        team_number = 2
        if len(args) >= 1:
            input_team_number = int(args[0])
            if input_team_number < 2 or input_team_number > 4:
                await ctx.send('❌ El numero de equipos debe ser entre 2 y 4')
                return
            team_number = input_team_number
                
        await ctx.send(f'_Creando {team_number} equipos aleatorios con los miembros de {ctx.channel.name}_')
        
        members = ctx.author.voice.channel.members
        teams : list[list[discord.Member]] = [[] for _ in range(team_number)]
        actual_team_idx = 0
        while len(members) > 0:
            member_choice = choice(members)
            teams[actual_team_idx].append(member_choice)
            members.remove(member_choice)
            actual_team_idx = (actual_team_idx + 1) % team_number
            
        response = ''
        for t_num, t in enumerate(teams, 1):
            response += f'**Equipo {t_num}**:\n'
            for m in t:
                response += f'{m.display_name}\n'
            if t_num < team_number: response += '\n'
            
        await ctx.send(response)
            
async def setup(bot : commands.Bot):
    try:
        cog = Rng(bot)
        await bot.add_cog(cog)
    except Exception as e:
        logger.error(f'Error loading {cog.qualified_name} cog')