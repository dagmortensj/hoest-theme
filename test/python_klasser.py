# Python: klasser, dekoratorer, typer, async og match
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar
import numpy as np

T = TypeVar("T")

@dataclass(frozen=True)
class Legeme(Generic[T]):
    """Et legeme med masse og posisjon."""
    navn: str
    masse: float = 1.0
    posisjon: np.ndarray = field(default_factory=lambda: np.zeros(2))

    def __post_init__(self) -> None:
        if self.masse <= 0:
            raise ValueError(f"Masse må være positiv: {self.masse}")

    @property
    def er_tung(self) -> bool:
        return self.masse > 1e3 and self.__class__.__name__ != "Sol"

    @classmethod
    def fra_tekst(cls, tekst: str) -> Legeme:
        navn, masse = tekst.split(";")
        return cls(navn, float(masse))

async def hent(url: str, *, tidsavbrudd: int = 10) -> bytes:
    async with økt.get(url) as svar:
        return await svar.read()

match kommando.split():
    case ["flytt", x, y]: print(int(x), int(y))
    case {"fart": float(v)} if v > 0: print(Legeme("a").er_tung)
    case _: pass
