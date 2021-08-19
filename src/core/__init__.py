import sys
import asyncio

if sys.platform == "linux":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


from .botbase import *
from .database import *
