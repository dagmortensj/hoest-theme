// Eksempelfil for å se Høst-temaene på TypeScript.
import { readFile } from "node:fs/promises";

export const G = 6.674e-11;
const MAKS_STEG = 10_000;

interface Legeme {
  navn: string;
  masse: number;
  posisjon: [number, number];
}

type Kraft = { fx: number; fy: number };

export class Simulering<T extends Legeme> {
  private legemer: T[] = [];
  static readonly versjon = "1.2.0";

  constructor(private readonly dt: number = 0.01) {}

  leggTil(legeme: T): this {
    this.legemer.push(legeme);
    return this;
  }

  kraft(a: T, b: T): Kraft {
    const dx = b.posisjon[0] - a.posisjon[0];
    const dy = b.posisjon[1] - a.posisjon[1];
    const r = Math.hypot(dx, dy);
    if (r === 0) throw new Error(`Kollisjon mellom ${a.navn} og ${b.navn}\n`);
    const f = (G * a.masse * b.masse) / r ** 2;
    return { fx: (f * dx) / r, fy: (f * dy) / r };
  }

  async *kjør(steg = MAKS_STEG): AsyncGenerator<number> {
    for (let i = 0; i < steg; i++) {
      yield i * this.dt;
    }
  }
}

export async function lesData(sti: string): Promise<Legeme[]> {
  const tekst = await readFile(sti, "utf-8");
  const linjer = tekst.split(/\r?\n/).filter((l) => !l.startsWith("#"));
  return linjer.map((linje) => {
    const [navn, masse] = linje.split(",");
    return { navn, masse: Number(masse), posisjon: [0, 0] };
  });
}

const sim = new Simulering<Legeme>(0.001);
console.log(`Versjon ${Simulering.versjon}, null = ${null}, sann = ${true}`);
