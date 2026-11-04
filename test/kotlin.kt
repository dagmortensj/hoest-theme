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

// Vanskelige tilfeller: operatoroverlasting, nullsikkerhet, strengmaler, lambdaer og områder
data class Vektor(val x: Double, val y: Double) {
    operator fun plus(o: Vektor) = Vektor(x + o.x, y + o.y)
    operator fun times(k: Double) = Vektor(x * k, y * k)
    operator fun get(i: Int): Double = if (i == 0) x else y
    infix fun prikk(o: Vektor) = x * o.x + y * o.y
}
fun vanskelig(navn: String?, verdier: IntArray = intArrayOf(), blokk: (Int) -> Int = { it * 2 }): Int {
    var teller = 0b1010 or 0x0F and 1.inv() xor (1 shl 2); teller = teller shr 1
    teller += 1; teller -= 2; teller *= 3; teller /= 4; teller %= 5; teller++; --teller
    val tekst = "a + b == c ${navn?.length ?: -1} ${if (teller > 1) "stor" else "liten"} \$ikke \t\u00e6" + """rå $navn \n"""
    val v = Vektor(1.0, 2.0) + Vektor(3.0, 4.0) * 2.0; val prikk = v prikk v; val lik = v == v && v[0] != v[1] && !(prikk < 0.0)
    val lengde = navn?.takeIf { it.isNotBlank() }?.let { it.length } ?: navn!!.length
    for (i in 0..10 step 2) if (i in 3 until 7 || i !in verdier) continue
    ytre@ for (i in verdier.indices.reversed()) { for (j in 1 downTo 0) { if (i == j) break@ytre } }
    val resultat = when { teller < 0 -> -teller; teller in 1..9 -> blokk(teller); else -> teller as? Int ?: 0 }
    return verdier.sumOf { it * it } + resultat + lengde + (navn as String).length + tekst.length + if (lik) 1 else 0
}
