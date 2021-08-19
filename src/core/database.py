from __future__ import annotations

import typing as t

import asyncpg

from ..utils import Config

__all__ = ("Database",)


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool

    @classmethod
    async def create_pool(cls: t.Type[Database], config: Config) -> Database:
        self = cls()
        self.pool = await asyncpg.create_pool(  # type: ignore
            database=config["DB"]["name"],
            user=config["DB"]["user"],
            password=config["DB"]["password"],
        )

        with open("schema.sql") as file:
            await self.pool.execute(file.read())  # type: ignore

        return self

    async def execute(self, query: str, *args, timeout: float = None) -> str:
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args, timeout: float = None) -> list:
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(
        self, query: str, *args, timeout: float = None
    ) -> asyncpg.Record:
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)
