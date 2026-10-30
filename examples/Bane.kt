// Eksempelfil for å se Høst-temaene på Kotlin.
package no.fysikk.bane

import kotlin.math.hypot

const val G = 6.674e-11

data class Legeme(val navn: String, val masse: Double, var x: Double = 0.0, var y: Double = 0.0)

sealed interface Resultat {
    data class Kraft(val verdi: Double) : Resultat
    object Kollisjon : Resultat
}

class Simulering(private val dt: Double = 0.01) {
    private val legemer = mutableListOf<Legeme>()

    fun leggTil(legeme: Legeme) = apply { legemer += legeme }

    fun kraft(a: Legeme, b: Legeme): Resultat {
        val r = hypot(b.x - a.x, b.y - a.y)
        return when {
            r == 0.0 -> Resultat.Kollisjon
            else -> Resultat.Kraft(G * a.masse * b.masse / (r * r))
        }
    }
}

fun main() {
    val sim = Simulering().leggTil(Legeme("Sola", 1.989e30))
    for (i in 0 until 3) {
        println("Steg $i: ${sim.hashCode()}\n")
    }
    val ingenting: String? = null
    println(ingenting ?: "tom")
}
