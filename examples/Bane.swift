// Eksempelfil for å se Høst-temaene på Swift.
import Foundation

let G = 6.674e-11

struct Legeme: Identifiable, Equatable {
    let id = UUID()
    var navn: String
    var masse: Double
    var posisjon: (x: Double, y: Double) = (0, 0)

    static func == (a: Legeme, b: Legeme) -> Bool { a.id == b.id }
}

enum Feil: Error {
    case kollisjon(String, String)
}

final class Simulering {
    private(set) var legemer: [Legeme] = []
    weak var delegat: AnyObject?

    func kraft(_ a: Legeme, _ b: Legeme) throws -> Double {
        let r = hypot(b.posisjon.x - a.posisjon.x, b.posisjon.y - a.posisjon.y)
        guard r > 0 else { throw Feil.kollisjon(a.navn, b.navn) }
        return G * a.masse * b.masse / (r * r)
    }
}

let sola = Legeme(navn: "Sola", masse: 1.989e30)
for i in 0..<3 {
    print("Steg \(i): \(sola.navn)\n", terminator: "")
}
let tom: String? = nil
print(tom ?? "ingen", true)
