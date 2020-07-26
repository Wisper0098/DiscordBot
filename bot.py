import discord
from discord.ext import commands
import config
import webbrowser
import items_parser
import datetime
import time_script

client = discord.Client()
bot = commands.Bot(command_prefix="/")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

@bot.command()
async def google(ctx, arg):
    url = f"https://www.google.com/search?q={arg}"
    webbrowser.open(url)
    await ctx.send('Found')

@bot.command()
async def vote(ctx, question=None, arg1=None, arg2=None):
    if question == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали вопрос.\nПример: `(Вопрос ? Аргумент1, Аргумент2)`')
        await ctx.send(embed=emb)

    elif arg1 == None or arg2 == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали аргументы.\nПример: `(Вопрос ? Аргумент1, Аргумент2)`')
        await ctx.send(embed=emb)
    
    else:
        full_message = ctx.message.content
        qstion = full_message[5:full_message.index("?")-1] # question, example: How ?
        variant1 = full_message[full_message.index("?")+1:full_message.index(",")]
        variant2 = full_message[full_message.index(",")+1:]
        emb = discord.Embed(title=f"Голосование от: {ctx.author.name}",colour=discord.Color.blue())
        emb.add_field(name=qstion, value=f'\n1️⃣{variant1}\n2️⃣ {variant2}')
        message = await ctx.send(embed=emb)
        await message.add_reaction('1️⃣')
        await message.add_reaction('2️⃣')


@bot.command()
async def get_cats(ctx, server=None, item_name=None): # типа /get_cats_info "Название предмета", "сервер"
    if server == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали сервер.\nПример: `("Сервер" "Предмет")`')
        await ctx.send(embed=emb)

    elif item_name == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали имя предмета.\nПример: `("Сервер" "Предмет")`')
        await ctx.send(embed=emb)

    else:
        if items_parser.parse(server, item_name) == False: # if server is not defined
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=ctx.author.name, value='Сервер не найден')
            await ctx.send(embed=emb)

        elif items_parser.parse(server, item_name) == "Предмет не найден": # if item is not defined
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=ctx.author.name, value='Предмет не найден')
            await ctx.send(embed=emb)

        else:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=f"Предмет: {item_name}", value=f'{items_parser.parse(server, item_name)}')
            await ctx.send(embed=emb)
        
        
bot.run(config.TOKEN)