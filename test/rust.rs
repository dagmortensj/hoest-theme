// Rust: strukturer, egenskaper, livstider, makroer og mønstre
use std::collections::HashMap;
use std::fmt::{self, Display};

const G: f64 = 6.674e-11;
static mut TELLER: u32 = 0;
#[derive(Debug, Clone, PartialEq)]
pub struct Legeme<'a> {
    pub navn: &'a str,
    masse: f64,
}

pub enum Hendelse { Start, Kollisjon { a: usize, b: usize }, Slutt(i32) }

pub trait Kraft {
    fn kraft(&self, annen: &Self, r: f64) -> Result<f64, String>;
}

impl<'a> Kraft for Legeme<'a> {
    fn kraft(&self, annen: &Self, r: f64) -> Result<f64, String> {
        if r == 0.0 { return Err(format!("{} kolliderer", self.navn)); }
        Ok(G * self.masse * annen.masse / r.powi(2))
    }
}

impl Display for Legeme<'_> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "{}\n", self.navn) }
}

fn main() {
    let mut kart: HashMap<String, Vec<u8>> = HashMap::new();
    let jord = Legeme { navn: "Jorda", masse: 5.972e24 };
    match jord.kraft(&jord, 1.0) { Ok(f) if f > 0.0 => println!("{f:.2e}"), _ => {} }
    let tunge: Vec<_> = (0..10).filter(|&x| x % 2 == 0).map(|x| x as f64).collect();
    unsafe { TELLER += 1 }; kart.insert(String::from("a"), vec![0xFF, b'x']);
}
