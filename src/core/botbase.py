from __future__ import annotations

import os

import aiohttp
import datetime
import typing as t

import discord
from discord.ext import commands

from .database import Database
from ..utils import Config


class _0x42(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            self.get_prefix,
            intents=discord.Intents.default(),
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
        )
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.startup: datetime.datetime = datetime.datetime.utcnow()
        self.config: Config = Config.from_file("config.yml")
        self.owner_ids: t.List[int] = [self.config["BOT"]["owner_ids"]]
        self.database: Database

        self.loop.create_task(self._create_database())
        self.load_extension("jishaku")

    async def _create_database(self) -> None:
        try:
            self.database = await Database.create_pool(self.config)
            print("[0x42] Database is ready")
        except Exception as e:
            raise e

    async def get_prefix(self, message: discord.Message) -> str:
        if message.guild is not None:
            return (
                await self.database.fetchrow(
                    "SELECT prefix FROM guilds WHERE id = $1", message.guild.id
                )
            )[0]

        return self.config["BOT"]["prefix"]

    async def on_guild_join(self, guild: discord.Guild) -> str:
        return await self.database.execute(
            "INSERT INTO guilds (id, prefix) VALUES ($1, $2)",
            guild.id,
            str(self.config["BOT"]["prefix"]),
        )

    async def on_ready(self) -> None:
        print("[0x42] Bot is ready")

    async def on_guild_remove(self, guild: discord.Guild) -> str:
        return await self.database.execute("DELETE FROM guilds WHERE id = $1", guild.id)

    def run(self, *args, **kwargs) -> None:
        for ext in [
            f"src.exts.{ext[:-3]}"
            for ext in os.listdir("src/exts")
            if ext[:-3] == ".py"
        ]:
            self.load_extension(ext)
        super().run(self.config["BOT"]["token"], *args, **kwargs)

    async def close(self) -> None:
        await self.session.close()
        await self.database.pool.close()
        return await super().close()


Bot: t.Type[_0x42] = _0x42
