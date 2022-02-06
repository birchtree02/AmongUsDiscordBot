import discord
from discord.ext import commands

cogs = ["cogs.channel-management"]

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

with open("token.txt", "r") as file:
    TOKEN = file.read()

with open("authenticated_users.txt", "r") as file:
    authenticated_users = file.readlines()
    for (i, user) in enumerate(authenticated_users):
        authenticated_users[i] = int(user)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


@bot.command(hidden=True)
async def reload(ctx, cog):
    if ctx.author.id in authenticated_users:
        try:
            bot.reload_extension(f"cogs.{cog}")
            print(f"\nRELOADED {cog}.\n")
            return await ctx.send(f"{cog} successfully reloaded")
        except Exception as e:
            return await ctx.send(e)
    else:
        return await ctx.channel.send("You are not a boi.")

if __name__ == "__main__":
    for extension in cogs:
        bot.load_extension(extension)

    bot.run(TOKEN, bot=True, reconnect=True)
