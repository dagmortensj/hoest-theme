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

# Vanskelige tilfeller: numpy, parametere i kroppen, dekoratorer med argumenter og typer
import functools
from numpy.linalg import norm
norm2 = np.linalg.norm  # variabel som holder en funksjon: grønn med Pylance
Matrise = np.ndarray | None
class Simulering(Legeme[float]):
    teller: int = 0
    @staticmethod
    def steg(v: np.ndarray, a: np.ndarray, dt: float = 1e-3) -> np.ndarray:
        return v + a*dt - np.sqrt(np.abs(v)) * np.pi  # overlastede operatorer på arrays
    @functools.lru_cache(maxsize=None)
    def energi(self, fart: float, *, høyde: float = 0.0) -> float:
        fart = abs(fart); Simulering.teller += 1
        return 0.5 * self.masse * fart**2 + self.masse * 9.81 * høyde
    def __matmul__(self, annen: Simulering) -> float: return float(self.posisjon @ annen.posisjon)
    def __contains__(self, punkt: tuple[float, float]) -> bool: return punkt in self.posisjon
sim = Simulering("sol", masse=2e30)
print((1.0, 2.0) in sim, sim @ sim, sim.energi(fart=3.0, høyde=2.0), Simulering.steg(np.zeros(2), np.ones(2)))
async def strøm(kilde: AsyncIterator[bytes], antall: int = 3) -> list[bytes]:
    return [bit async for bit in kilde if len(bit) > antall][:antall]
match sim:
    case Simulering(masse=m) if m > 1e29: print("stjerne", norm(sim.posisjon) - norm2(sim.posisjon))
