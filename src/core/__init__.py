import sys
import asyncio

if sys.platform == "linux":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


from .botbase import *
from .database import *

@client.command()
async def iscatgirl(ctx, user :discord.Member):
        if user.name =="mudkip":
            await ctx.message.channel.send("yes")
        else:
            await ctx.message.channel.send("no")
