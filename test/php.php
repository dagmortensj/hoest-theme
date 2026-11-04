<?php
// PHP: klasser, egenskaper, navnerom, typer og strenger
declare(strict_types=1);

namespace Hoest\Fysikk;

use InvalidArgumentException;
use function array_map;

const G = 6.674e-11;

enum Farge: string { case Rod = 'R'; case Gronn = 'G'; }

interface Legeme { public function masse(): float; }

#[\Attribute]
final class Planet implements Legeme
{
    public static int $antall = 0;

    public function __construct(
        private readonly string $navn,
        protected float $masse = 1.0,
    ) { self::$antall += 1; $tekst = 'Planet'; $tekst .= $navn; }

    public function masse(): float { return $this->masse; }

    public function kraft(?Planet $annen, float ...$r): float|int
    {
        if ($annen === null) throw new InvalidArgumentException("Mangler {$this->navn}\n");
        $liste = array_map(fn($x) => $x ** 2, [1, 2, 3]);
        return match (true) { $r[0] > 0 => G * $this->masse / $r[0], default => 0 };
    }
}

echo "Antall: " . Planet::$antall, PHP_EOL, sprintf('%05.2f', 3.14159);

// Vanskelige tilfeller: operatorer, strenger, lukninger, matcher og typer
abstract class Vanskelig extends Planet implements \Countable, \Stringable
{
    public const int|float MAKS = 1_000 + 0x0F | 0b1010 ^ 1 << 2;
    protected static ?self $instans = null;
    public function __construct(private array $verdier = [], public readonly string $navn = 'x') { parent::__construct($navn); }
    public function count(): int { return count($this->verdier); }
    public function __toString(): string
    {
        $tekst = "a + b == c {$this->navn} ${navn} $this->navn \t\u{E6}" . 'apostrof \'x\' $ikke' . <<<TEKST
            Her-dokument med {$this->navn} og \t
            TEKST . <<<'RÅ'
            rå $tekst \n
            RÅ;
        return $tekst;
    }
    public static function lag(mixed ...$args): static { return self::$instans ??= new static(...$args); }
    abstract protected function regn(int $a, int &$b, ?float $c = null): int|false;
    public function test(): bool
    {
        $t = 0; $t += 1; $t -= 2; $t *= 3; $t /= 4; $t %= 5; $t **= 2; $t .= 'x'; $t ??= 0; $t <<= 1; $t |= 1; $t ^= 2; $t &= ~3;
        $lik = $t == 1 || $t === '1' && $t !== null and $t <=> 2 or !$t xor $t <> 3; $neg = -$t + +$t % 2 ** 3;
        $f = fn(int $x): int => $x * 2 + $t; $g = function ($y) use (&$t, $f): int { return $f($y) - $t++; };
        $liste = [1, 2, ...$this->verdier, 'nøkkel' => 3]; ['nøkkel' => $n, 0 => $første] = $liste;
        foreach ($liste as $nøkkel => &$verdi) { if ($verdi instanceof self || $nøkkel <=> 1) continue; else break; }
        return match (true) { $t > 1, $t < -1 => $lik, default => (bool) $g($n + $første) ?: $neg > 0 };
    }
}
