# Python: det elevene skriver mest
"""Docstring for modulen."""
import math
from random import randint as tilfeldig

G = 9.81  # tyngdeakselerasjon
masser = [1.0, 2.5, 0x1F, 1_000, 3e-4, 2j, -7]
navn = 'Ada'
ferdig = True and not False or None

def fall(h: float, v0: float = 0.0, *args, **kwargs) -> float:
    """Tiden det tar å falle h meter."""
    return (-v0 + math.sqrt(v0**2 + 2*G*h)) / G


for i in range(len(masser)):
    if i % 2 == 0 and masser[i] > 1:
        continue
    elif i == 3:
        break
    else:
        pass

h = float(input("Høyde: "))
print(f"Tid: {fall(h):.2f} s for {navn!r}\n", end="")
print("%d meter, %s" % (int(h), str(h)), r"\n er rå", b"bytes")
kvadrater = [x**2 for x in range(10) if x in {1, 2}]
data = {"masse": 2.0, 'fart': -3, "liste": list(), "par": tuple()}
kvadrat = lambda x: x * x
try:
    tilfeldig(1, 6) / 0
except ZeroDivisionError as feil:
    raise ValueError("deling på null") from feil
finally:
    del kvadrater
assert isinstance(h, float), "feil type"
