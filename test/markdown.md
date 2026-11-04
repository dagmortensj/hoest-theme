# Overskrift 1

## Overskrift 2 med `kode`

Avsnitt med **fet**, *kursiv*, ***begge***, ~~gjennomstreket~~ og `innebygd kode`.
En [lenke](https://example.com "Tittel"), en <https://example.com> og et bilde:
![Alternativ tekst](bilde.png)

> Et sitat over
> to linjer, med **fet** tekst.

- Punkt
- Punkt med [referanse][1]
  - Underpunkt
1. Nummerert
2. Liste
- [x] Ferdig oppgave
- [ ] Uferdig oppgave

| Kolonne | Høyre |
|:--------|------:|
| a       | 1     |

---

```python
def hei(navn: str) -> None:
    print(f"Hei, {navn}!\n")
```

Matte: $E = mc^2$ og $$\int_0^1 x\,dx$$

<details><summary>HTML i Markdown</summary>Skjult</details>

[1]: https://example.com

## Vanskelige tilfeller

Setext-overskrift
-----------------

Tekst med a + b == c, `kode med **stjerner**`, ``kode med `apostrof` ``, \*unnslippet\*, _kursiv_ og __fet__.
Lenke med [tittel i parentes](https://example.com/(a)) og ![bilde][b], HTML-entitet &amp; og linjeskift  
etter to mellomrom. Fotnote[^1] og ~~gjennomstreket *kursiv*~~.

* Stjernepunkt
+ Plusspunkt
    1) Nummerert med parentes
    2) Og `inline`

> > Nestet sitat
> med `kode` og $x^2$

```ts
const f = (x: number): number => x * 2 + 1;  // kommentar
```

    Innrykket kodeblokk med x += 1

~~~
Tilde-blokk
~~~

| Tabell | med `kode` | og $m c^2$ |
|---|:-:|--:|
| **fet** | *kursiv* | [lenke](x) |

$$
\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}
$$

<div align="center"><img src="bilde.png" width="200"></div>

[^1]: Fotnotetekst.
[b]: bilde.png "Tittel"
