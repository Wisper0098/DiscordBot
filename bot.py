import discord
from discord.ext import commands, tasks
from discord import utils
import config
import webbrowser
import items_parser
import asyncio
import pymongo
from pymongo import MongoClient

#------------------------------------------
# db settings
client = MongoClient("mongodb+srv://nexxon028:1234@cluster0.umdee.mongodb.net/users?retryWrites=true&w=majority")
db = client['pwcats']        
coll = db['users']
#################
#------------------------------------------

client = discord.Client()
bot = commands.Bot(command_prefix="/")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

@bot.event
async def on_raw_reaction_add(payload):
        channel = bot.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        
        if str(payload.emoji) == "❌" and payload.user_id != bot.user.id:
            result = coll.find_one({"user_id": payload.user_id})
            isnotvote = 0
            old_val = {"isvote": result["isvote"]} 
            new_val = {"$set": {"isvote": 0}}
            coll.update_one(old_val, new_val) # update database value

            ##

            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=message.author.name, value='Успешно, заменено.\nНапишите /every_day_vote')
            await channel.send(embed=emb)
        
    
@bot.command()
async def start(ctx): # init this command when bot will be host
    while True:
        time = 3600
        await asyncio.sleep(time)
        await ctx.send("Напоминаем что у нас есть группа в VK https://vk.com/pw_tma")

@bot.command()
async def google(ctx, arg): # command for search in google
    argu = arg.replace(" ", "+")
    url = f"https://www.google.com/search?q={argu}"
    webbrowser.open(url)
    await ctx.send('Найдено')

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
async def get_cats(ctx, server=None, item_name=None): 
    
    if server == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали сервер.\nПример: `("Сервер" ! "Предмет")`')
        await ctx.send(embed=emb)

    elif item_name == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали имя предмета.\nПример: `("Сервер" ! "Предмет")`')
        await ctx.send(embed=emb)

    else:
        full_message = ctx.message.content
        serVer = full_message[10:full_message.index("!")-1]
        itm_name = full_message[full_message.index("!")+2:]
        
        if items_parser.parse(serVer, itm_name) == False: # if server is not defined
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=ctx.author.name, value='Сервер не найден')
            await ctx.send(embed=emb)

        elif items_parser.parse(serVer, itm_name) == "Предмет не найден": # if item is not defined
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=ctx.author.name, value='Предмет не найден')
            await ctx.send(embed=emb)

        else:
            full_message = ctx.message.content
            serVer = full_message[10:full_message.index("!")-1]
            itm_name = full_message[full_message.index("!")+1:]
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=f"Предмет: {itm_name}", value=f'{items_parser.parse(serVer, itm_name)}')
            await ctx.send(embed=emb)

@bot.command()
async def every_day_vote(ctx, question=None, arg1=None, arg2=None):

    if question == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали вопрос.\nПример: `(Вопрос ? Аргумент1, Аргумент2)`')
        await ctx.send(embed=emb)

    elif arg1 == None or arg2 == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали аргументы.\nПример: `(Вопрос ? Аргумент1, Аргумент2)`')
        await ctx.send(embed=emb)
    
    else:
        post = {"user_id": ctx.author.id, "isvote": 1}
        check = coll.find_one({"user_id": ctx.author.id})
        if check is None: # if user not create vote, create
            coll.insert_one(post) # add user to database
            ##
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=ctx.author.name, value='Успешно. \nГолосование будет проводиться каждые 24 часа.')
            await ctx.send(embed=emb)
            full_message = ctx.message.content
            qstion = full_message[15:full_message.index("?")-1] # question, example: How ?
            variant1 = full_message[full_message.index("?")+1:full_message.index(",")]
            variant2 = full_message[full_message.index(",")+1:]
            emb = discord.Embed(title=f"Голосование от: {ctx.author.name}",colour=discord.Color.blue())
            emb.add_field(name=qstion, value=f'\n1️⃣{variant1}\n2️⃣ {variant2}')
            while True: # sending poll every 24 hours
                time = 86400 # 24 hour in seconds                                                                                                                      #:D
                await asyncio.sleep(time) 
                message = await ctx.send(embed=emb)
                await message.add_reaction('1️⃣')                
                await message.add_reaction('2️⃣')
            
        if check["isvote"] == 0: # if user delete or not create vote
            ##
            result = coll.find_one({"user_id": ctx.author.id}) # search user in database
            old_val = {"isvote": result["isvote"]}
            new_val = {"$set": {"isvote": 1}}
            coll.update_one(old_val, new_val) # update db value
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=ctx.author.name, value='Успешно. \nГолосование будет проводиться каждые 24 часа.')
            await ctx.send(embed=emb)
            full_message = ctx.message.content
            qstion = full_message[15:full_message.index("?")-1] # question, example: How ?
            variant1 = full_message[full_message.index("?")+1:full_message.index(",")]
            variant2 = full_message[full_message.index(",")+1:]
            emb = discord.Embed(title=f"Голосование от: {ctx.author.name}",colour=discord.Color.blue())
            emb.add_field(name=qstion, value=f'\n1️⃣{variant1}\n2️⃣ {variant2}')
            while True:
                time = 86400 # 24 hour in seconds                                                                                                                      #:D
                await asyncio.sleep(time)
                message = await ctx.send(embed=emb)
                await message.add_reaction('1️⃣')                
                await message.add_reaction('2️⃣')
        ##
        elif check["isvote"] == 1: # if user already create vote.
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=ctx.author.name, value='Вы уже делали такое голосование.\nНажмите на "❌" чтобы отключить голосование.')
            mesage = await ctx.send(embed=emb)
            await mesage.add_reaction("❌")

bot.run(config.TOKEN)