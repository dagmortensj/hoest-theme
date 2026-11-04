// JavaScript: moduler, klasser, async og regulære uttrykk
import fs from "node:fs";
import { join as sti } from "node:path";
export const G = 6.674e-11;
let teller = 0, ferdig = false, tom = null, ukjent = undefined;
const tall = [0x1f, 0b1010, 0o17, 1_000n, .5, NaN, Infinity];

/**
 * Beregner kraften mellom to legemer.
 * @param {number} m1 Masse 1
 * @returns {number}
 */
function kraft(m1, m2 = 1, ...rest) {
  return (G * m1 * m2) / rest[0] ** 2;
}

class Planet extends Object {
  #hemmelig = 42;
  static antall = 0;
  constructor(navn) { super(); this.navn = navn; }
  get beskrivelse() { return `Planet ${this.navn}\t(${Planet.antall})`; }
  async *bane(steg) { for await (const s of steg) yield s; }
}

const dobbel = (x) => x * 2;
teller += 1; teller **= 2; teller ||= 1; ukjent ??= tom;
const { a, b: omdøpt, ...resten } = { a: 1, b: 2, c: 3 };
const mønster = /^(\d+)\s*[a-z]+$/gi;
if (typeof dobbel === "function" && dobbel instanceof Object) {
  console.log("Treff:", mønster.test("12 kg"), Math.max(...tall));
} else switch (teller) { case 0: break; default: throw new Error("feil"); }
try { JSON.parse("{}"); } catch (e) { console.error(e.message); }
fs.readFile(sti(".", "a.txt"), (feil, data) => void feil ?? data?.length);
export default Planet;

// Vanskelige tilfeller: regulære uttrykk, maler, operatorer og objekter
const re = /(\d+)\.(\d*)(?:e[-+]?\d+)?|\/=/g; const del = 1 / 2 / 3; const gen = function* () { yield* [1]; };
let n = 0; n += 1; n **= 2; n >>>= 1; n &&= 3; n ??= 4; n ||= 5; n = n++ + --n - -n;
const t = `a + b == ${n * 2 > 1 ? "ja" : `nei ${n}`} \` \${escape}`; const s = "x = y" + 'z' + "\u00e6\n";
const o = { "nøkkel med mellomrom": 1, 2: "to", [Symbol.iterator]: null, async *gen() {}, får: this?.x ?? 0 };
const p = o?.["nøkkel med mellomrom"] ?? o.får; const q = typeof p === "number" && p instanceof Number;
ytre: while (true) { for (const [k, v] of Object.entries(o)) { if (k in o && !(v === void 0)) break ytre; } }
class Stjerne extends Planet {
  static { Planet.antall = 0; }
  #masse = 1; get masse() { return this.#masse; }
  static lag(...args) { return new this(...args); } #privat() { return super.beskrivelse; } }
new Promise((løs, avvis) => setTimeout(løs, 1_000)).then((r) => r, (e) => { throw e; }).finally(() => {});
delete o[2]; export { Stjerne, re, t, o }; export * as alt from "./annen.js";
