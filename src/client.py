"""
            --- Charruo Bot ---
    Version: (en desarrollo)
    
    Codigo principal del bot
    
    https://github.com/lu1smgb/CharruoBot
"""

import environment

import discord
from discord.ext import commands

import datetime

class BotClient(discord.Client):
    
    # Constructor
    def __init__(self):
        
        self._intents = discord.Intents.default()
        self._intents.message_content = True
        
        self._bot = commands.Bot(command_prefix='!', intents=self._intents)
        
        self._logger = environment.logging.getLogger('bot')
        
        super().__init__(intents=self._intents)
        
        self.run(environment.BOT_TOKEN, root_logger=True)

    async def on_ready(self):
        """ 
        Invocado cuando el bot esta listo
        Realmente, el bot esta listo antes de que el mensaje llegue a imprimirse por consola
        """
        self._logger.info(f'Ready')
    
    async def generate_response(self, message: discord.Message):
        """
        Genera una respuesta/reaccion a un mensaje que ha leido el bot
        """
          
        async def insultar():
            """ Reacciona con 🖕 y le responde que se calle """
            await message.add_reaction('🖕')
            await message.reply(f'Callate ya <@{message.author.id}>')
            
        async def mewing():
            """ Reacciona con 🤫🧏‍♂️ """
            await message.add_reaction('🤫')
            await message.add_reaction('🧏‍♂️')
        
        # Solo insulta si el que escribe es Proxx
        if message.author.name == environment.PROXX_ID:
            await insultar()
        
        # El bot hace mewing si encuentra alguna de estas ocurrencias en el mensaje
        for substr in ['mewing', '🤫', '🧏‍♂️']:
            if message.content.lower().count(substr):
                await mewing()
    
    
    async def on_message(self, message : discord.Message):
        """
        Invocado cuando recibe un mensaje en el servidor
        """
        
        nickname : str = message.author.display_name
        user_id : int = message.author.id
        content : str = message.content
        
        if not content:
            self._logger.error("Couldnt be able to get the user message, make sure the intents are enabled properly")
            return
        
        # El bot no revisa sus propios mensajes
        if user_id == self.user.id:
            return
        
        # Imprime en consola el usuario y el contenido del mensaje
        print(f'{nickname}: {content}')
        
        # Genera una respuesta en base a los datos del mensaje
        await self.generate_response(message)
            
    async def on_typing(self, channel: discord.TextChannel, user: discord.Member | discord.User, datetime : datetime.datetime):
        """
        Invocado cuando alguien escribe en un canal
        """
        print(f'El usuario {user.display_name} esta escribiendo a las {datetime.time()} en el canal \"{channel}\"')
        
def main():
    """
    Para iniciar el bot, hay que ejecutar este script
    """
    BotClient()
        
if __name__ == "__main__":
    main()
    