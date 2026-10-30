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
