import asyncio
import json
from music import playlist

import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
import os

client = commands.Bot(command_prefix="!")
channels = dict()
general = dict()
playing = True

general["name"] = "general"
if not os.path.exists("general.pl"):
    with open("general.pl", "w") as f:
        f.write(json.dumps(general))

with open("general.pl", "r") as f:
    general = playlist.Playlist(f.read())


@client.event
async def on_ready():
    print("Bot online")

@client.command(pass_context=True)
async def join(ctx):
    voice = ctx.message.author.voice
    if voice is None:
        await ctx.message.reply("Join a Voicechannel")
    vc = await voice.channel.connect()
    channels[ctx.message.guild] = vc

@client.command(pass_context=True)
async def leave(ctx):
    try:
        await channels[ctx.message.guild].disconnect()
    except KeyError as e:
        await ctx.message.reply("Not in a Voicechannel")

@client.command()
async def play(ctx):
    vc = ""
    try:
        vc = channels[ctx.message.guild]
    except KeyError as e:
        await ctx.send("Use join first")
        return
    if vc.is_playing():
        await ctx.send("Already playing")
        return
    mes = ctx.message.content
    splitmes = mes.split(" ")[1:]
    if splitmes[0] == "url":
        await playbyurl(vc, splitmes[1])
    if splitmes[0] == "song":
        await playsong(ctx, vc, splitmes[1], splitmes[1:])
    if splitmes[0] == "playlist":
        await playplaylist(vc, splitmes[1], splitmes[1:])


@client.command()
async def add(ctx):
    mes = ctx.message.content
    splitmes = mes.split(" ")[1:]
    if splitmes[0] == "song":
        general.addSong(splitmes[1], splitmes[2])
    if splitmes[0] == "playlist":
        pass

@client.command()
async def stop(ctx):
    channels[ctx.message.guild].stop()

@client.command()
async def pause(ctx):
    channels[ctx.message.guild].pause()

@client.command()
async def resume(ctx):
    channels[ctx.message.guild].resume()

async def playbyurl(vc, url):
    ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    vc.is_playing()

async def playsong(ctx, vc, name, args):
    song = general.getSong(name)
    if song is None:
        await ctx.message.reply("No such Song")
    await playbyurl(vc, song.url)
    if "continue" in args:
        playing = True
        while playing:
            if vc.is_playing():
                await asyncio.sleep(1)
            else:
                n = general.getnext()
                await playbyurl(vc, n.url)


async def playplaylist(vc, name, args):
    pass


client.run("ODk5NzMyMDY0NTE2MDU1MTIw.YW3CyA._OWYlHw3kPpDJQD6tYBcHPlto8g")