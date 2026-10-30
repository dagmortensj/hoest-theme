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
  useEffect(() => { document.title = `${tittel} (${antall})`; }, [tittel]);

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
