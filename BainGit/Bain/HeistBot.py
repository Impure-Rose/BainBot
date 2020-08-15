import discord
from discord.ext import commands
from discord import VoiceChannel
import random 
import asyncio
import youtube_dl


import csv 
with open('Payday Decider Spreadsheet.csv', newline='') as csvfile:
        sheet= csv.reader(csvfile)
        rows=[r for r in sheet]
with open('The Heist Decider.csv', newline='')as spread:
        options=csv.reader(spread)
        contracts=[r for r in options]

with open('PD2Weapons.csv') as builds:
        fnet=csv.reader(builds)
        generator=[r for r in fnet]

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):

        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')

        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):

        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:

            # take first item from a playlist

            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)

        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

client= commands.Bot (command_prefix='!')

@client.event 
async def on_ready():
    print("The thermal drill go get it")

@client.command()
async def heist(ctx):
    step=random.randrange(1,75)
    job=rows[step]
    await ctx.send(f'{str(job[0])}')


@client.command()
async def contract(ctx):
    heist=random.randrange(8)
    await ctx.send(f'{str(contracts[heist])}')

@client.command(aliases=['gage','asspack'])
async def build(ctx):

    primaryNumb=random.randrange(114)
    secondaryNumb=random.randrange(62)
    perkNumb=random.randrange(1,22) 
    deployNumb=random.randrange(1,8)
    heisterNumb=random.randrange(1,23)
    meleeNumb=random.randrange(85)
    throwableNumb=random.randrange(16)
    armorNumb=random.randrange(1,8)
    primary=generator[primaryNumb]
    secondary=generator[secondaryNumb]
    perk=rows[perkNumb]
    deploy=rows[deployNumb]
    heister=rows[heisterNumb]
    melee=generator[meleeNumb]
    throwable=generator[throwableNumb]
    armor=rows[armorNumb]

    await ctx.send("Primary: "+primary[0] + ", Secondary: "+secondary[1] +", Perk Deck: "+perk[3]+ ", Deployable: "+deploy[4]+ ", Heister: "+heister[5]+ ", Melee: "+melee[2]+", Throwable: "+throwable[3]+ ", Armor: "+armor[8])
    

@client.command(aliases=['asspacksm','smasspack','gagesm','smgage','smbuild'])
async def buildsm(ctx):
    primaryNumb=random.randrange(114)
    secondaryNumb=random.randrange(62)
    perkNumb=random.randrange(1,22) 
    primary=generator[primaryNumb]
    secondary=generator[secondaryNumb]
    perk=rows[perkNumb]
    await ctx.send("Primary: "+primary[0] + ", Secondary: "+secondary[1]+", Perk Deck: "+perk[3] )



    
@client.command()
async def info(ctx):
    await ctx.send("Commands:\n !heist-Picks a heist in Payday2\n !contract- picks a heist in Payday The Heist\n !build- generates a build for Payday 2\n !buildsm- generates a smaller build\n !bye- disconnects from VC\n !meme- connect to VC\n !pd2 +Song_Name- Plays a song from Payday\n !stream + link- streams audio from a link")
    await ctx.send("Memes:\n !orange, !ineed, !gogetit, !pickle, !pizzatime")

#Currently in development 
class Cook_Off(commands.Cog):

    def __init__(self,client):
        self.client=client
    @commands.command()
    async def cookoff(self, ctx):
        await ctx.send("We're going to need ingredients.")
        ingredients=["caustic soda", "muriatic acid","hydrogen chloride"]
        async with ctx.typing():
            ingredientNeeded=ingredients[random.randrange(0,2)]
            
        await ctx.send("hydrogen chloride, muriaic acid, and caustic soda")
            




class AudioPlayer(commands.Cog):

    def __init__(self,client):
        self.client=client
    @commands.command()
    async def meme(self,ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        if ctx.voice_client is not None:
                await ctx.voice_client      
        
    @commands.command()
    async def bye(self,ctx):
        await ctx.voice_client.disconnect()

    @commands.command(aliases=["thisissosad"])
    async def thatssosad(self,ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="BainsPlaylist/Razormind.mp3"))

    @commands.command()
    async def pickle(self,ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="BainsPlaylist/Chains_is_in_a_Pickle.mp3"))

    @commands.command()
    async def pizzatime(self,ctx):  
        url="https://www.youtube.com/watch?v=czTksCF6X8Y"
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        player=await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        ctx.voice_client.play(player)

    @commands.command(aliases=["ThermalDrill","Guys"])
    async def gogetit(self, ctx):
        url="https://www.youtube.com/watch?v=vsW2sYiChCo"
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        player=await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        ctx.voice_client.play(player)

    @commands.command(aliases=["medicbag","MedicBag","MediBag"])
    async def ineed(self, ctx):
        url="https://www.youtube.com/watch?v=kAM3gVEEcqo"
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        player=await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        ctx.voice_client.play(player)
    
    @commands.command()
    async def healing(self, ctx):
        url="https://youtu.be/Ze8vJ8JSfn4"
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        player=await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        ctx.voice_client.play(player)
    
    @commands.command(aliases=["dejavu"])
    async def DejaVu(self, ctx):
        url="https://youtu.be/dv13gl0a-FA"
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        player=await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        ctx.voice_client.play(player)

    @commands.command()
    async def orange(self, ctx):
        url="https://www.instagram.com/p/rptmLPzakW/?hl=en"
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        player=await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
        ctx.voice_client.play(player)

    @commands.command()
    async def fwb(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="C:ffmpeg/bin/ffmpeg.exe", source="BainsPlaylist/Gun_Metal_Grey.mp3"))



    @commands.command()
    async def stream(self, ctx, *, url): 
        async with ctx.typing():
            if ctx.voice_client is None:
                await ctx.author.voice.channel.connect()
            player=await YTDLSource.from_url(url,loop=self.client.loop, stream=True)
            ctx.voice_client.play(player)
        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def pd2(self, ctx,*,song):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="BainsPlaylist/"+song+".mp3"))

async def stream(self, ctx, url):
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    player=await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
    ctx.voice_client.play(player)



client.add_cog(AudioPlayer(client))
client.add_cog(Cook_Off(client))

