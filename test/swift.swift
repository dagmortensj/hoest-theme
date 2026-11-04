// Swift: strukturer, klasser, protokoller, utvidelser og async
import Foundation

let G = 6.674e-11
var teller: Int = 0x1F

protocol Legeme {
    var navn: String { get }
    var masse: Double { get set }
    func kraft(fra annen: Self, avstand r: Double) -> Double
}

struct Planet: Legeme, Codable {
    let navn: String
    var masse: Double = 1.0
    func kraft(fra annen: Planet, avstand r: Double) -> Double {
        G * masse * annen.masse / (r * r)
    }
}

enum Farge: String, CaseIterable { case rød = "R", grønn }

@MainActor
final class Simulering<T: Legeme> {
    private(set) var legemer: [T] = []
    lazy var navn = "Standard"
    init(legemer: [T] = []) { self.legemer = legemer }

    func kjør(steg: Int = 10) async throws -> Double? {
        guard !legemer.isEmpty else { throw NSError(domain: "tom", code: 1) }
        let tunge = legemer.filter { $0.masse > 1e24 }.map(\.navn)
        for i in 0..<steg where i % 2 == 0 { print("Steg \(i): \(tunge.count)\n") }
        if let første = legemer.first { return første.masse } else { return nil }
    }
}
extension Double { var kvadrat: Double { self * self } }

// Vanskelige tilfeller: operatoroverlasting, valgfrie verdier, lukninger, strenger og områder
struct Vektor: Equatable {
    var x = 0.0, y = 0.0
    static func + (a: Vektor, b: Vektor) -> Vektor { Vektor(x: a.x + b.x, y: a.y + b.y) }
    static func * (a: Vektor, k: Double) -> Vektor { Vektor(x: a.x * k, y: a.y * k) }
    static prefix func - (a: Vektor) -> Vektor { Vektor(x: -a.x, y: -a.y) }
    subscript(i: Int) -> Double { i == 0 ? x : y }
}
infix operator •: MultiplicationPrecedence
func • (a: Vektor, b: Vektor) -> Double { a.x * b.x + a.y * b.y }
func vanskelig(_ navn: String?, verdier: [Int] = [], med blokk: (Int) throws -> Int = { $0 * 2 }) rethrows -> Int {
    var bits = 0b1010 | 0x0F & ~1 ^ 1 << 2; bits >>= 1; bits += 1; bits -= 2; bits *= 3; bits /= 4; bits %= 5; bits &+= 1
    let tekst = "a + b == c \(navn?.count ?? -1) \(bits > 1 ? "stor" : "liten") \t\u{E6}" + #"rå \n \#(bits)"# + """
        flere linjer
        """
    let v = Vektor(x: 1, y: 2) + Vektor(x: 3, y: 4) * 2 + -Vektor(); let lik = v == v && v[0] != v[1] && !(v • v < 0)
    guard let n = navn, !n.isEmpty, case let antall? = Optional(n.count) else { return 0 }
    for i in stride(from: 0, through: 10, by: 2) where i % 3 == 0 { if (3..<7).contains(i) || 0...10 ~= i { continue } }
    ytre: for i in verdier.indices.reversed() { for j in (0...1).reversed() { if i == j { break ytre } } }
    let resultat = switch bits { case ..<0: -bits; case 1...9: try blokk(bits); default: (bits as Int?) ?? 0 }
    return verdier.reduce(0) { $0 + $1 * $1 } + resultat + antall + tekst.count + (lik ? 1 : 0) + n.count
}
