import discord
import environment
from random import random

async def generate_response(message: discord.Message):
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
    
    # Solo insulta si el que escribe es Proxx, con una probabilidad del 10%
    if message.author.name == environment.PROXX_ID and random.random() < 0.1:
        await insultar()
    
    # El bot hace mewing si encuentra alguna de estas ocurrencias en el mensaje
    for substr in ['mewing', '🤫', '🧏‍♂️']:
        if message.content.lower().count(substr):
            await mewing()
            break