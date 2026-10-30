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
