// Eksempelfil for å se Høst-temaene på C#.
using System;
using System.Collections.Generic;
using System.Linq;

namespace Fysikk.Bane;

public record Legeme(string Navn, double Masse, double X, double Y);

public sealed class Simulering
{
    public const double G = 6.674e-11;
    private readonly List<Legeme> _legemer = new();

    public int Antall => _legemer.Count;

    public void LeggTil(Legeme legeme) => _legemer.Add(legeme);

    public double Kraft(Legeme a, Legeme b)
    {
        var r = Math.Sqrt(Math.Pow(b.X - a.X, 2) + Math.Pow(b.Y - a.Y, 2));
        if (r is 0) throw new InvalidOperationException($"Kollisjon mellom {a.Navn} og {b.Navn}\n");
        return G * a.Masse * b.Masse / (r * r);
    }

    public async Task<Legeme?> TyngstAsync()
    {
        await Task.Delay(10);
        return _legemer.OrderByDescending(l => l.Masse).FirstOrDefault();
    }

    public static void Main(string[] args)
    {
        var sim = new Simulering();
        sim.LeggTil(new Legeme("Sola", 1.989e30, 0, 0));
        foreach (var steg in Enumerable.Range(0, 3))
            Console.WriteLine($"Steg {steg}: {sim.Antall} legemer, ferdig = {false}");
    }
}
