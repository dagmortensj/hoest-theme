// Eksempelfil for å se Høst-temaene på JavaScript og JSX.
import { useState, useEffect } from "react";

const G = 6.674e-11;

export function Bane({ legemer, dt = 0.01 }) {
  const [tid, setTid] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setTid((t) => t + dt), 16);
    return () => clearInterval(id);
  }, [dt]);

  const tyngst = legemer.reduce((a, b) => (a.masse > b.masse ? a : b), null);

  return (
    <section className="bane" data-tid={tid.toFixed(2)}>
      <h2>Tid: {tid.toFixed(1)} s</h2>
      {tyngst && <p>Tyngst: {tyngst.navn}</p>}
      <ul>
        {legemer.map((l) => (
          <li key={l.navn}>{`${l.navn}: ${l.masse.toExponential(2)} kg`}</li>
        ))}
      </ul>
    </section>
  );
}

export default class Simulering {
  #legemer = [];
  static versjon = "1.0";

  async hent(url) {
    const svar = await fetch(url);
    if (!svar.ok) throw new Error(`Feil: ${svar.status}`);
    this.#legemer = await svar.json();
    return this;
  }
}
