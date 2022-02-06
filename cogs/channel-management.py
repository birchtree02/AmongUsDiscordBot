import discord
from discord.ext import commands


class ChannelManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.game_state = None

    async def check_in_game(self, ctx):
        for player in self.players:
            if not self.players[player]["obj"].voice:
                self.players.remove([player])
        if self.game_state is not None:
            if ctx.author.id in self.players.keys():
                return True
            else:
                await self.send(ctx, "You are not in the game.")
        else:
            await self.output_game_state(ctx, "No Game Started")

    async def output_game_state(self, ctx, title=""):
        playerNames = '\n'.join([self.players[player]['obj'].name for player in self.players if self.players[player]['dead']])
        if playerNames:
            playerNames = '\n*(dead)*\n'+playerNames
        playerNames = ('*(alive)*\n' if playerNames else '') + \
            '\n'.join([self.players[player]['obj'].name for player in self.players if not self.players[player]['dead']]) \
            + playerNames
        if not playerNames:
            playerNames = '*No players*'

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name=f"{title if title else 'Game In Progress'}")

        embed.add_field(name="**Players**", value=f"{playerNames}", inline=False)
        embed.add_field(name="**Game**", value=f"*In {self.game_state}*")
        await ctx.send(embed=embed)

    @commands.command(name='resetplayers', aliases=['reset', 'lobby', 'newgame'])
    async def reset_players(self, ctx, *args):
        if ctx.author.voice:
            self.game_state = "lobby"
            self.players = {}

            members = ctx.author.voice.channel.members

            for m in members:
                self.players[m.id] = {"obj": m, "dead": False}

            for player in self.players:
                await self.players[player]["obj"].edit(mute=False)
                await self.players[player]["obj"].edit(deafen=False)

            if args and "end" in args[0].lower():
                self.players = {}
                self.game_state = None
                await self.output_game_state(ctx, "No Game Started")
            else:
                await self.output_game_state(ctx, "New Game Created")

        else:
            await self.send(ctx, "This is not allowed. You are not in a voice channel.")

    @commands.command(name='killplayer', aliases=['dead'])
    async def kill_player(self, ctx):
        if await self.check_in_game(ctx):
            if self.game_state != "lobby":
                self.players[ctx.author.id]["dead"] = True
                if self.game_state == "game":
                    await self.deafen_alive_players(ctx)
                elif self.game_state == "meeting":
                    await self.undeafen_alive_mute_dead(ctx)
            else:
                await self.output_game_state(ctx, "No Game Started")


    @commands.command(name='deafenalive', aliases=['game'])
    async def deafen_alive_players(self, ctx):
        if await self.check_in_game(ctx):
            self.game_state = "game"
            for player in self.players:
                if not self.players[player]["dead"]:
                    await self.players[player]["obj"].edit(deafen=True)
                else:
                    await self.players[player]["obj"].edit(mute=False)
            await self.output_game_state(ctx)

    @commands.command(name='undeafenalivemutedead', aliases=['meeting'])
    async def undeafen_alive_mute_dead(self, ctx):
        if await self.check_in_game(ctx):
            self.game_state = "meeting"
            for player in self.players:
                await self.players[player]["obj"].edit(deafen=False)
                if self.players[player]["dead"]:
                    await self.players[player]["obj"].edit(mute=True)
            await self.output_game_state(ctx)

    # Moves all members from the author's voice channel to the given voice channel
    @commands.command(name='moveall', aliases=['ma'])
    async def move_all(self, ctx, *args):
        if ctx.author.voice:
            channel = ctx.author.voice.channel

            members = channel.members
            target_channel = args[0]

            if target_channel.lower() == "none":
                for member in members:
                    await member.move_to(None)
                await self.send(ctx, f"Removed {len(members)} from voice.")
            else:
                for channel in self.bot.get_all_channels():
                    if type(channel) == discord.channel.VoiceChannel:
                        if channel.name == target_channel:
                            for member in members:
                                await member.move_to(channel)
                            await self.send(ctx, f"Moved {len(members)} to {target_channel}.")
                            break
                else:
                    await self.send(ctx, f"Channel {target_channel} was not found.")
        else:
            await self.send(ctx, "This is not allowed. You are not in a voice channel.")

    async def send(self, ctx, msg):
        await ctx.send(msg)
        print(f"sent: {msg}")


def setup(bot):
    bot.add_cog(ChannelManagementCog(bot))
