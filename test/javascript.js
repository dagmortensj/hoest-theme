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
const { a, b: omdøpt, ...resten } = { a: 1, b: 2, c: 3 };
const mønster = /^(\d+)\s*[a-z]+$/gi;
if (typeof dobbel === "function" && dobbel instanceof Object) {
  console.log("Treff:", mønster.test("12 kg"), Math.max(...tall));
} else switch (teller) { case 0: break; default: throw new Error("feil"); }
try { JSON.parse("{}"); } catch (e) { console.error(e.message); }
fs.readFile(sti(".", "a.txt"), (feil, data) => void feil ?? data?.length);
export default Planet;
