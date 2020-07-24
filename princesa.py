import os

import discord
from dotenv import load_dotenv
from gtts import gTTS
from discord.ext import commands
import os

class Princesa(discord.Client):
    async def on_ready(self):
        self.shark_tank_guild_id = 249450178350809088
        self.shark_tank_general_channel_id = self.shark_tank_guild_id
        print('Logged in as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower().startswith('hello') or (message.content.lower().find('good') != -1 and (message.content.lower().find('morning') != -1 or message.content.lower().find('night') != -1)):
            await message.channel.send('Bark')
        
        if message.content.lower().startswith('say'):
            voice_client = await message.author.voice.channel.connect()
            tts = gTTS(text=message.content.split("#")[1], lang='en')
            tts.save('tts.mp3')
            voice_client.play(discord.FFmpegPCMAudio('tts.mp3'))
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
            voice_client.source.volume = 1.0

            while True:
                if voice_client.is_playing():
                    pass
                else:
                    await voice_client.disconnect()
                    break

    async def on_guild_join(self, guild):
        text_channels = guild.text_channels
        await text_channels[0].send('Welcome to the Shark Tank!')

    async def on_voice_state_update(self, member, before, after):
        if before.channel == None and after.channel != None:
            await self.get_guild(self.shark_tank_guild_id).get_channel(self.shark_tank_general_channel_id).send(str(member.name) + ' just joined ' + str(after.channel.name))


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = Princesa()
client.run(TOKEN)
