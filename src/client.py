"""
            --- Charruo Bot ---
    Version: (en desarrollo)
    
    Codigo principal del bot
    
    https://github.com/lu1smgb/CharruoBot
"""

import discord
from discord.ext import commands

import datetime
import secrets
import random

import environment
import responses

logger = environment.logging.getLogger('bot')

class CharruoBot2(commands.Bot):
    
    def __init__(self):
        """
        Constructor
        """
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        """
            ----- EVENTOS -----
        """
        @self.event
        async def on_ready():
            logger.info(f'Ready as {self.user}')
            
        @self.event
        async def on_message(message: discord.Message):
            """
            Invocado cuando recibe un mensaje en el servidor
            """
            # El bot no revisa sus propios mensajes
            if message.author == self.user:
                return
            
            # En caso de que el mensaje no se pueda leer debido a los intents
            if not message.content:
                logger.error("No se pudo leer el mensaje debido a que el bot no posee los \"intents\" necesarios")
                return
            
            # Imprime en consola el usuario y el contenido del mensaje
            print(f'[#{message.channel}] {message.author.display_name}\n\t{message.content}')
            
            # El bot procesa los comandos que hayan podido escribirse
            await self.process_commands(message)
            
            # Genera una respuesta en base a los datos del mensaje
            await responses.generate_response(message)
            
        # on_typing event R.I.P
            
        """
            ----- COMANDOS (PROVISIONAL) -----
        """
        @self.command()
        async def ping(ctx: commands.Context):
            """
            Manda un ping al bot
            """
            response = 'Pong 🏓'
            await ctx.send(response)
            
        @self.command()
        async def github(ctx: commands.Context):
            """
            Muestra el GitHub del bot
            """
            await ctx.send('Aqui esta el repositorio con el codigo del bot:\nhttps://github.com/lu1smgb/CharruoBot')
            
        @self.command()
        async def rng(ctx: commands.Context):
            """
            Genera un decimal aleatorio entre 0 y 1
            """
            number = random.random()
            await ctx.send(f'Ha salido el numero: {number}')
            
        @self.command()
        async def dado(ctx: commands.Context, *args):
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
                    await ctx.send('❌ No voy a tirar dados de dos caras, pa eso tiro monedas 😐')
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
            resultados = [('[' + str(random.randint(1,caras)) + ']') for _ in range(veces)]
            await ctx.send(', '.join(resultados))
                    
        @self.command()
        async def moneda(ctx: commands.Context, *args):
            raise NotImplementedError("Comando por implementar")
            
        # Iniciamos el bot
        self.run(environment.BOT_TOKEN, root_logger=True)

# -------------------------------------------------------------------------------------------------
        
def main():
    CharruoBot2()
    
if __name__ == "__main__":
    main()

            