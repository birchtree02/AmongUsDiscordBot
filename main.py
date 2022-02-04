import discord
from discord.ext import commands

cogs = []

bot = commands.Bot(command_prefix='!')

with open("token.txt", "r") as file:
    TOKEN = file.read()

with open("authenticated_users.txt", "r") as file:
    authenticated_users = file.readlines()
    print(authenticated_users)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


@bot.command(hidden=True)
async def reload(ctx, cog):
    if ctx.author.id in authenticated_users:    
        try:
            bot.reload_extension(f"cogs.{cog}")
            return await ctx.send(f"{cog} successfully reloaded")
        except Exception as e:
            return await ctx.send(e)
    else:
        return await ctx.channel.send("You are not a boi.")

if __name__ == "__main__":
    for extension in cogs:
        bot.load_extension(extension)

    bot.run(TOKEN, bot=True, reconnect=True)