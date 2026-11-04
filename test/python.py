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
    h /= tilfeldig(0, 6); h **= 2
except ZeroDivisionError as feil:
    raise ValueError("deling på null") from feil
finally:
    del kvadrater
assert isinstance(h, float), "feil type"

# Vanskelige tilfeller: operatorer, strenger, parametere og uttrykk
def kraft(m1: float, m2: float, /, r: float = 1.0, *, konstant: float = G) -> float:  # m1, m2 bare posisjonelt
    """Operatorer i docstring: a + b == c."""
    global masser
    return -konstant * m1 * m2 / r**2 if r != 0 else float("inf")
teller = 0; teller += 1; teller -= 2; teller **= 2; teller //= 3; teller %= 4; teller <<= 1; teller |= 1; A @= B
tekst = "a + b == c and not d"  # operatorer i strengen skal være blå, som i denne kommentaren: x -= 1
mal = f"{teller + 1:>{len(navn)}} {teller=} {navn!r} {G:.3e} {{bokstavelig}} {'nestet' if teller else ''}"
rå = r"\d+\s*(?P<enhet>kg|m)"; byte = b"\x00\xff"; bred = "\u00e6\N{DEGREE SIGN}"; lang = """flere
linjer med "sitat" og 'apostrof'"""
innenfor = 0 < teller <= 10 and teller not in (1, 2) and navn is not None or not ferdig
skive = masser[1:-1:2]; matrise = A @ B; biter = ~0x0F & 0b1010 | 1 << 2 ^ 3 >> 1; neg = -teller + +teller
if (n := len(masser)) > 3: print(n, *masser, sep=", ", end="\n")
ferdig = (lambda x=1, *a, **k: x * 2)(2) if ferdig else None
with open("fil.txt", encoding="utf-8") as fil, open("ut.txt", "w") as ut: ut.write(fil.read())
def teller_opp(start: int):
    yield from range(start); yield -1
class Vektor(tuple):
    __slots__ = ()
    def __add__(self, annen: "Vektor") -> "Vektor": return Vektor(a + b for a, b in zip(self, annen))
    def __eq__(self, annen: object) -> bool: return tuple(self) == tuple(annen)
v = Vektor((1, 2)) + Vektor((3, 4)); print(v == (4, 6), v.__class__, type(v).__name__, kraft(1, 2, r=3))
