import environment

import discord
from discord.ext import commands
# import bot_commands

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
    
    # Cuando el bot esta listo para funcionar
    # En realidad esta listo antes de imprimir el mensaje
    async def on_ready(self):
        self._logger.info(f'Ready')
    
    # Cuando se envia un mensaje en un servidor
    async def on_message(self, message : discord.Message):
        
        user : str = message.author.name
        nickname : str = message.author.display_name
        user_id : int = message.author.id
        content : str = message.content
        server_id: int = message.guild.id
        
        if not content:
            self._logger.error("Couldnt be able to get the user message, make sure the intents are enabled properly")
            return
        
        # El bot no revisa sus propios mensajes
        if user_id == self.user.id:
            return
        
        # Imprime en consola el usuario y el contenido del mensaje
        print(f'{nickname}: {content}')
        
        # TODO: Crear funcion para generar una respuesta
        
        # Si Proxx es el autor, le dice que se calle
        if user == environment.PROXX_ID and server_id == environment.TEST_SERVER_ID:
            await message.add_reaction('🖕')
            await message.reply(f'Callate ya <@{message.author.id}>')
            return
            
    # Cuando una persona escribe en un canal
    async def on_typing(self, channel: discord.TextChannel, user: discord.Member | discord.User, datetime : datetime.datetime):
        print(f'El usuario {user.display_name} esta escribiendo a las {datetime.time()} en el canal \"{channel}\"')
        
def main():
    BotClient()
        
if __name__ == "__main__":
    main()
    