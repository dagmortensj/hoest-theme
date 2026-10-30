// Eksempelfil for å se Høst-temaene på Java.
package no.fysikk.bane;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public final class Simulering {
    public static final double G = 6.674e-11;
    private static final int MAKS_STEG = 10_000;

    public record Legeme(String navn, double masse, double x, double y) {}

    private final List<Legeme> legemer = new ArrayList<>();
    private boolean aktiv = false;

    @Override
    public String toString() {
        return "Simulering med %d legemer\n".formatted(legemer.size());
    }

    public Optional<Legeme> tyngst() {
        return legemer.stream().max((a, b) -> Double.compare(a.masse(), b.masse()));
    }

    public double kraft(Legeme a, Legeme b) throws ArithmeticException {
        double r = Math.hypot(b.x() - a.x(), b.y() - a.y());
        if (r == 0) {
            throw new ArithmeticException("Kollisjon mellom " + a.navn() + " og " + b.navn());
        }
        return G * a.masse() * b.masse() / (r * r);
    }

    public static void main(String[] args) {
        var sim = new Simulering();
        sim.legemer.add(new Legeme("Sola", 1.989e30, 0, 0));
        for (int i = 0; i < MAKS_STEG && sim.aktiv; i++) {
            System.out.println(sim);
        }
        char tegn = 'J';
        Object ingenting = null;
    }
}
