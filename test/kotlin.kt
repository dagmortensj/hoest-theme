// Kotlin: klasser, dataklasser, utvidelser, lambdaer og korutiner
package no.hoest.fysikk

import kotlin.math.sqrt
import kotlinx.coroutines.*

const val G = 6.674e-11

data class Legeme(val navn: String, var masse: Double = 1.0)

enum class Farge(val kode: Int) { ROD(1), GRONN(2) }

sealed interface Hendelse
object Start : Hendelse

@JvmInline
value class Meter(val verdi: Double)

fun Double.kvadrat(): Double = this * this

class Simulering<T : Legeme>(private val dt: Double) {
    private val legemer = mutableListOf<T>()
    lateinit var navn: String
    val antall: Int get() = legemer.size

    fun legg(vararg nye: T): Simulering<T> = apply { legemer += nye }

    suspend fun kjør(steg: Int = 10) = coroutineScope {
        for (i in 0 until steg) {
            val tunge = legemer.filter { it.masse > 1e24 }.map { l -> l.navn }
            println("Steg $i: ${tunge.size} tunge, ${sqrt(dt)}\n")
        }
        when (antall) { 0 -> null; in 1..9 -> "få"; else -> throw IllegalStateException() }
    }
    companion object { fun lag() = Simulering<Legeme>(0.01) }
}
