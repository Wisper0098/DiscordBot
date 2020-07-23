import discord
from discord.ext import commands
import config

client = discord.Client()
bot = commands.Bot(command_prefix="/")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

@bot.command()
async def vote(ctx, question=None, arg1=None, arg2=None):
    if question == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали вопрос.\nПример: `(Вопрос ? Аргумент1, Аргумент2)`')
        await ctx.send(embed=emb)

    if arg1 == None or arg2 == None:
        emb = discord.Embed(colour=discord.Color.red())
        emb.add_field(name=ctx.author.name, value='Вы не указали аргументы.\nПример: `(Вопрос ? Аргумент1, Аргумент2)`')
        await ctx.send(embed=emb)
    
    else:
        full_message = ctx.message.content
        qstion = full_message[5:full_message.index("?")] # question, example: How ?
        variant1 = full_message[full_message.index("?")+1:full_message.index(",")]
        variant2 = full_message[full_message.index(",")+1:]
        emb = discord.Embed(title=f"Голосование от: {ctx.author.name}",colour=discord.Color.green())
        emb.add_field(name=qstion, value=f'\n1️⃣{variant1}\n2️⃣ {variant2}')
        await ctx.send(embed=emb)




bot.run(config.TOKEN)