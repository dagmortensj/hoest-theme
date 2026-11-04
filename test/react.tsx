// React med TSX: komponenter, props, hooks og JSX
import React, { useState, useEffect } from "react";
import type { FC, ReactNode } from "react";
import "./stil.css";

interface Props {
  tittel: string;
  antall?: number;
  children?: ReactNode;
  vedKlikk: (id: number) => void;
}

export const Kort: FC<Props> = ({ tittel, antall = 0, children, vedKlikk }) => {
  const [åpen, settÅpen] = useState<boolean>(false);
  useEffect(() => { let n = antall; n += 1; document.title = `${tittel} (${n})`; }, [tittel]);

  return (
    <section className="kort" data-id={antall} aria-label="Kort">
      {/* Kommentar inne i JSX */}
      <h2 style={{ color: "red", fontSize: 14 }}>{tittel}</h2>
      {åpen && <p>Innhold: {children}</p>}
      <ul>
        {[1, 2, 3].map((n) => (
          <li key={n} onClick={() => vedKlikk(n)}>Element {n}</li>
        ))}
      </ul>
      <Knapp deaktivert={!åpen} onClick={() => settÅpen(!åpen)} />
      <React.Fragment>&nbsp;&copy; 2026</React.Fragment>
    </section>
  );
};

function Knapp(props: { deaktivert: boolean; onClick(): void }) {
  return <button disabled={props.deaktivert} {...props}>Trykk</button>;
}

// Vanskelige tilfeller: generiske komponenter, betingelser og operatorer i JSX
type ListeProps<T> = { elementer: readonly T[]; velg?: (e: T, i: number) => boolean; tittel?: string };
export function Liste<T extends { id: number }>({ elementer, velg = () => true, tittel = "Liste" }: ListeProps<T>) {
  const [valgt, settValgt] = useState<T | null>(null);
  const synlige = elementer.filter((e, i) => velg(e, i) && e.id % 2 === 0).sort((a, b) => a.id - b.id);
  const tekst = `${synlige.length} av ${elementer.length}`;
  useEffect(() => { let teller = 0; teller += synlige.length; document.title = tekst + (teller > 5 ? "!" : ""); }, [tekst]);
  return (
    <>
      <h3 className={valgt ? "aktiv" : undefined} data-antall={synlige.length - 1}>{tittel} ({tekst})</h3>
      {synlige.length === 0 ? <p>Ingen &mdash; {"a + b == c"} {`mal ${1 + 1}`}</p> : (
        <ol start={1} reversed={false}>
          {synlige.map((e, i) => <li key={e.id} onClick={() => settValgt(valgt?.id === e.id ? null : e)}>#{i + 1}: {e.id}</li>)}
        </ol>
      )}
      <Kort tittel={tittel} antall={synlige.length * 2} vedKlikk={(id) => id > 0 && settValgt(null)}><b>x</b></Kort>
    </>
  );
}
