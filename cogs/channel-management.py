import discord
from discord.ext import commands


class ChannelManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dead_players = []


    # Moves all members from the author's voice channel to the given voice channel
    @commands.command(name='moveall', aliases=['ma'])
    async def move_all(self, ctx, *args):
        if ctx.author.voice:
            channel = ctx.author.voice.channel

            members = channel.members
            target_channel = args[0]

            print(members[0].id)
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
            await self.send(ctx, f"This is not allowed. You are not in a voice channel.")

    async def send(self, ctx, msg):
        await ctx.send(msg)
        print(f"sent: {msg}")


def setup(bot):
    bot.add_cog(ChannelManagementCog(bot))