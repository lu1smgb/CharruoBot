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

class CharruoBot(commands.Bot):
    
    def __init__(self):
        """
        Constructor
        """
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='%', intents=intents)
        
        """
            ----- EVENTOS -----
        """
        @self.event
        async def on_ready():
            # Carga los cogs en la carpeta 'cmd'
            for cog_file in environment.COG_DIR.glob("*.py"):
                if cog_file != "__init__.py":
                    logger.info(f'Loading cog {cog_file.name[:-3]}')
                    await self.load_extension(f"{environment.COG_DIR.name}.{cog_file.name[:-3]}")
            
            # Indica que esta todo listo para su uso
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
        @self.event
        async def on_command_error(ctx: commands.Context, error):
            if isinstance(error, commands.errors.CommandNotFound):
                await ctx.send('❌ El comando no existe')
            
        """
            ----- COMANDOS (PROVISIONAL) -----
        """
        @self.command()
        async def github(ctx: commands.Context):
            """
            Muestra el GitHub del bot
            """
            await ctx.send('Aqui esta el repositorio con el codigo del bot:\nhttps://github.com/lu1smgb/CharruoBot')
            
        # Iniciamos el bot
        self.run(environment.BOT_TOKEN, root_logger=True)

# -------------------------------------------------------------------------------------------------
        
def main():
    CharruoBot()
    
if __name__ == "__main__":
    main()

            