// C#: navnerom, klasser, records, egenskaper, LINQ og async
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Fysikk.Bane;

public enum Farge { Rød, Grønn = 2 }
public record Legeme(string Navn, double Masse);

[Serializable]
public sealed class Simulering<T> : IDisposable where T : Legeme
{
    public const double G = 6.674e-11;
    private readonly List<T> _legemer = new();
    public int Antall => _legemer.Count;
    public string? Navn { get; init; } = "Standard";
    public event EventHandler<T>? Lagt;

    public Simulering<T> Legg(T legeme)
    {
        _legemer.Add(legeme ?? throw new ArgumentNullException(nameof(legeme)));
        Lagt?.Invoke(this, legeme);
        return this;
    }

    public async Task<double> TotalAsync(int steg = 10, params int[] ekstra)
    {
        await Task.Delay(steg);
        var tunge = from l in _legemer where l.Masse > 1e24 select l.Masse;
        return _legemer.Sum(l => l.Masse) + tunge.Count() is > 0 ? 1.0 : 0.0;
    }

    public void Dispose() => Console.WriteLine($"{Navn}: {Antall:D3}\n" + @"C:\sti");
}

// Vanskelige tilfeller: operatorer, mønstre, LINQ, strenger og egenskaper
public readonly record struct Vektor(double X, double Y)
{
    public static Vektor operator +(Vektor a, Vektor b) => new(a.X + b.X, a.Y + b.Y);
    public static bool operator ==(Vektor a, Vektor b) => a.X == b.X && a.Y == b.Y;
    public static bool operator !=(Vektor a, Vektor b) => !(a == b);
    public double this[int i] => i switch { 0 => X, 1 => Y, _ => throw new IndexOutOfRangeException() };
    public double Lengde => Math.Sqrt(X * X + Y * Y);
}
public static class Vanskelig
{
    public static int Teller { get; private set; } = 0b1010 | 0x0F;
    public static T? Første<T>(this IEnumerable<T> kilde, Func<T, bool>? test = null) where T : class
        => kilde.FirstOrDefault(x => test?.Invoke(x) ?? true);
    public static string Beskriv(object? o, int antall = 1, params string[] ekstra)
    {
        Teller += 1; Teller <<= 2; Teller >>= 1; Teller ^= 0xF; Teller |= 1; Teller &= ~2; Teller %= 7;
        var tekst = $"a + b == c {antall * 2:N1} {{bokstavelig}} {(antall > 1 ? "flere" : "én")}" + @"\rå\sti" + "\t";
        return o switch
        {
            Legeme { Masse: > 1e24 } l => $"tung {l.Navn}",
            int i and (> 0 or < -10) => (i * 2 + -i).ToString(),
            null => tekst ?? string.Empty,
            _ when ekstra.Length is > 0 and < 10 => ekstra[^1],
            _ => nameof(o) + typeof(Vektor).Name + sizeof(int) + default(int),
        };
    }
}
