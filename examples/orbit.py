"""Simulerer banen til en planet rundt sola med Euler-Cromers metode."""
import matplotlib.pyplot as plt
import numpy as np

GM = 4 * np.pi**2   # AU^3/år^2, når massen til sola er 1
DT = 0.001          # tidssteg i år
SLUTT = 2.0         # simuleringstid i år


def akselerasjon(r):
    """Gravitasjonsakselerasjonen fra sola i punktet r."""
    avstand = np.linalg.norm(r)
    return -GM * r / avstand**3


def simuler(r0, v0, dt=DT, slutt=SLUTT):
    n = int(slutt / dt)
    r = np.zeros((n, 2))
    v = np.zeros((n, 2))
    r[0], v[0] = r0, v0
    for i in range(n - 1):
        v[i + 1] = v[i] + akselerasjon(r[i]) * dt
        r[i + 1] = r[i] + v[i + 1] * dt
        if np.linalg.norm(r[i + 1]) < 0.01:
            print(f"Kollisjon etter {i * dt:.2f} år")
            return r[: i + 2]
    return r


if __name__ == "__main__":
    for fart in [5.0, 2 * np.pi, 7.5]:
        bane = simuler(np.array([1.0, 0.0]), np.array([0.0, fart]))
        plt.plot(bane[:, 0], bane[:, 1], label=f"v0 = {fart:.2f} AU/år")
    plt.plot(0, 0, "o", color="orange", label="Sola")
    plt.axis("equal")
    plt.xlabel("x (AU)")
    plt.ylabel("y (AU)")
    plt.legend()
    plt.show()
