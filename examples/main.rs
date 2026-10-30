// Eksempelfil for å se Høst-temaene på Rust.
use std::fmt;

const G: f64 = 6.674e-11;
const MAKS_STEG: usize = 10_000;

#[derive(Debug, Clone, PartialEq)]
pub struct Legeme {
    pub navn: String,
    pub masse: f64,
    pub posisjon: (f64, f64),
}

#[derive(Debug)]
pub enum Feil {
    Kollisjon { mellom: (String, String) },
    TomListe,
}

impl fmt::Display for Feil {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Feil::Kollisjon { mellom: (a, b) } => write!(f, "kollisjon mellom {a} og {b}\n"),
            Feil::TomListe => write!(f, "ingen legemer"),
        }
    }
}

impl Legeme {
    pub fn kraft(&self, annet: &Legeme) -> Result<f64, Feil> {
        let (dx, dy) = (annet.posisjon.0 - self.posisjon.0, annet.posisjon.1 - self.posisjon.1);
        let r = dx.hypot(dy);
        if r == 0.0 {
            return Err(Feil::Kollisjon { mellom: (self.navn.clone(), annet.navn.clone()) });
        }
        Ok(G * self.masse * annet.masse / r.powi(2))
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let sola = Legeme { navn: "Sola".into(), masse: 1.989e30, posisjon: (0.0, 0.0) };
    let mut jorda = Legeme { navn: String::from("Jorda"), masse: 5.972e24, posisjon: (1.496e11, 0.0) };
    for i in 0..MAKS_STEG {
        let f = jorda.kraft(&sola)?;
        println!("steg {i}: F = {f:.3e} N, tegn = {}", 'J');
        jorda.posisjon.1 += 1.0;
        if i > 2 { break; }
    }
    Ok(())
}
