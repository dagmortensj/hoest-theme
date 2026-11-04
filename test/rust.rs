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

// Vanskelige tilfeller: operatoroverlasting, livstider, lukninger, makroer og mønstre
use std::ops::{Add, Mul};
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd, Default)]
pub struct Vektor { pub x: f64, pub y: f64 }
impl Add for Vektor { type Output = Self; fn add(self, o: Self) -> Self { Self { x: self.x + o.x, y: self.y + o.y } } }
impl Mul<f64> for Vektor { type Output = Self; fn mul(self, k: f64) -> Self { Self { x: self.x * k, y: self.y * k } } }
macro_rules! kvadrat { ($x:expr) => { $x * $x }; }
pub fn vanskelig<'a, T: Display + ?Sized>(navn: &'a T, verdier: &mut [i64], flagg: Option<&'a str>) -> impl Fn(i64) -> i64 + 'a {
    let tekst = format!("a + b == c {navn} {:>8.2} {{}}", 1.0f64) + r"rå \n" + "\u{e6}\t" + &'x'.to_string();
    let mut bits = 0b1010u8 | 0x0F & !1 ^ 1 << 2; bits >>= 1; bits %= 7; bits &= !0; let neg = -(bits as i32) + 1;
    for v in verdier.iter_mut() { *v += neg as i64; *v -= 1; *v *= 2; *v /= 3; *v <<= 1; *v |= 1; *v ^= 0xFF; }
    let (a, b) = (Vektor::default() + Vektor { x: 1.0, y: 2.0 } * 2.0, kvadrat!(3));
    let lik = a == a && b != 0 && !(a < a) || matches!(flagg, Some("x" | "y"));
    let s = match verdier { [første, .., siste] if første < siste => *siste - *første, [eneste] => *eneste, [] => 0 };
    if let Some(n) = flagg.and_then(|f| f.parse::<i64>().ok()).filter(|n| *n > 0) { println!("{n}"); }
    let spenn = 0..=10; let sum: i64 = spenn.clone().step_by(2).map(|i| i * i).sum::<i64>() + s + lik as i64;
    'ytre: loop { for _ in spenn { break 'ytre; } }
    move |x| x * 2 + sum
}
