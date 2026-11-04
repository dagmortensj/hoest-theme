// Java: pakker, klasser, grensesnitt, generiske typer og annotasjoner
package no.hoest.fysikk;

import java.util.*;
import java.util.function.Function;
import static java.lang.Math.sqrt;

@FunctionalInterface
interface Kraft { double beregn(double m1, double m2); }

record Legeme(String navn, double masse) {}

enum Farge { ROD, GRONN; String kort() { return name().substring(0, 1); } }

abstract sealed class Base permits Simulering {}

final class Simulering<T extends Legeme> extends Base implements Iterable<T> {
    public static final double G = 6.674e-11;
    private final List<T> legemer = new ArrayList<>();
    private int teller = 0x1F;

    @Override
    public Iterator<T> iterator() { return legemer.iterator(); }

    @SuppressWarnings("unchecked")
    public synchronized <R> R kart(Function<? super T, R> f, int... ekstra) {
        if (legemer.isEmpty()) throw new IllegalStateException("tom");
        for (T l : legemer) { teller++; teller ^= 0x1F; teller >>>= 1; }
        var tekst = """
            Tekstblokk med %d legemer\n""".formatted(legemer.size());
        Kraft k = (a, b) -> G * a * b / sqrt(2.0);
        return switch (teller) { case 0 -> null; default -> f.apply(legemer.get(0)); };
    }

    public static void main(String[] args) { System.out.println(args.length > 0); }
}

// Vanskelige tilfeller: operatorer, generiske typer, lambdaer, tekstblokker og annotasjoner
class Vanskelig<K extends Comparable<? super K>, V> {
    private static final Map<String, List<Integer>> KART = new HashMap<>();
    int teller = 0b1010 | 0x0F & ~0; long lang = 1_000_000L; double d = 1.5e-3d; float f = .5f; char c = '\u00e6';
    @Deprecated(since = "1.2", forRemoval = true) @SafeVarargs
    static <T> boolean test(T... verdier) { return verdier.length > 0 && verdier[0] != null; }
    String beskriv(Object o) {
        teller += 1; teller <<= 2; teller >>>= 1; teller ^= 0xF; teller |= 1; teller &= ~2; teller %= 7;
        var tekst = "a + b == c" + " ikke operatorer " + (teller > 1 ? "stor" : "liten") + 'x' + "\t\"";
        return switch (o) {
            case Legeme l when l.masse() > 1e24 -> "tung %s".formatted(l.navn());
            case Integer i -> String.valueOf(i * 2 + -i);
            case null, default -> tekst;
        };
    }
    void løkke() {
        ytre: for (int i = 0, j = 10; i < j; i++, j--) { if (i % 3 == 0) continue ytre; else break ytre; }
        Runnable r = () -> { synchronized (this) { teller++; } };
        Function<Integer, Function<Integer, Integer>> add = a -> b -> a + b;
        assert add.apply(1).apply(2) == 3 : "feil"; Object o = r instanceof Runnable rr ? rr : null;
    }
}
