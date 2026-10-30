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
let v: Kanskje<Vektor> = null;
const f = async <U,>(x: U): Promise<U> => await Promise.resolve(x);
function erTall(x: unknown): x is number { return typeof x === "number"; }
const kart = new Map<string, Array<boolean>>([["a", [true]]]);
export { Base, kart, path, type Readable };
