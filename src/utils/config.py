from __future__ import annotations

import typing as t

import yaml

__all__ = ("Config",)


class Config:
    def __init__(self, file: str):
        with open(file) as f:
            self.data = yaml.load(f, Loader=yaml.Loader)

    @classmethod
    def from_file(cls: t.Type[Config], file: str) -> Config:
        return cls(file)

    def __getitem__(self, key: t.Union[str, int]) -> t.Any:
        return self.data[key]
