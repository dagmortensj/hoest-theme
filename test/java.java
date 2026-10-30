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
        for (T l : legemer) { teller++; }
        var tekst = """
            Tekstblokk med %d legemer\n""".formatted(legemer.size());
        Kraft k = (a, b) -> G * a * b / sqrt(2.0);
        return switch (teller) { case 0 -> null; default -> f.apply(legemer.get(0)); };
    }

    public static void main(String[] args) { System.out.println(args.length > 0); }
}
