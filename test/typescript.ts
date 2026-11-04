// TypeScript: typer, grensesnitt, generiske typer og dekoratorer
import type { Readable } from "node:stream";
import * as path from "node:path";

export enum Retning { Opp = 1, Ned, Venstre = "V" }
type Vektor = readonly [number, number];
type Kanskje<T> = T | null | undefined;

interface Legeme {
  navn: string;
  masse?: number;
  readonly posisjon: Vektor;
  oppdater(dt: number): void;
}

function logg(mål: unknown, kontekst: ClassMethodDecoratorContext) {}

abstract class Base<T extends Legeme, K = string> {
  protected liste: T[] = [];
  private static readonly MAKS: number = 100;
  constructor(public readonly id: K) {}
  @logg
  legg(legeme: T): this { this.liste.push(legeme); return this; }
  abstract finn(navn: string): T | undefined;
}

declare const globalt: Record<string, unknown>;
namespace Fysikk { export const c = 299_792_458; }
const verdi = globalt["x"] as unknown as number;
const tekst = `${Fysikk.c} m/s` satisfies string;
let v: Kanskje<Vektor> = null; v ??= [0, 0];
let n = 1; n **= 2; n <<= 3; n >>>= 1;
const f = async <U,>(x: U): Promise<U> => await Promise.resolve(x);
function erTall(x: unknown): x is number { return typeof x === "number"; }
const kart = new Map<string, Array<boolean>>([["a", [true]]]);
export { Base, kart, path, type Readable };

// Vanskelige tilfeller: operatorer i typer og uttrykk, maler, regulære uttrykk og klasser
type Par<A, B = A> = A extends string ? `${A}-${B & string}` : [A, B] | null;
type Nøkler = keyof Legeme & string; type Valgfri<T> = { [K in keyof T]?: T[K] };
const mønster = /^(\d+)\s*(kg|m)$/giu; const deling = 10 / 2 / 1; const ikke = !v && !!verdi;
let sum = 0; sum += 1; sum -= 2; sum *= 3; sum /= 4; sum %= 5; sum **= 2; sum ??= 0; sum ||= 1; sum &&= 2;
const tekst = "a + b == c" + `mal med ${sum * 2 + (sum > 1 ? 1 : -1)} og \${ikke}` + 'apostrof \'x\'';
const streng = sum > 0 ? sum <= 10 ? "liten" : "stor" : sum === 0 ? "null" : typeof sum;
const bit = (0xff & 0x0f) | (1 << 2) ^ (~sum >>> 1); const neg = -sum ** 2; const inkr = sum++ + ++sum;
function sum2(...tall: number[]): number { return tall.reduce((a, b) => a + b, 0); }
const obj = { a: 1, "b-c": 2, [`d${sum}`]: 3, f() { return this.a; }, get g() { return 1; }, ...globalt };
const { a, "b-c": bc = 0, ...resten } = obj; const [x = 1, , y] = [1, 2, 3];
class Punkt<T extends number = number> implements Legeme {
  static #antall = 0; declare readonly posisjon: Vektor; navn = "p"; override toString(): string { return ""; }
  constructor(private x: T, public y: T = x) { Punkt.#antall++; }
  oppdater(dt: number): void { this.x = (this.x + dt * 2) as T; }
}
enum Flagg { A = 1 << 0, B = 1 << 1, AB = A | B }
for (let i = 0, j = 10; i < j; i++, j--) { if (i % 3 === 0) continue; }
ytre: for (const k in obj) { if (k === "a") break ytre; }
