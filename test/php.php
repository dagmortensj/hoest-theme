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
    ) { self::$antall++; }

    public function masse(): float { return $this->masse; }

    public function kraft(?Planet $annen, float ...$r): float|int
    {
        if ($annen === null) throw new InvalidArgumentException("Mangler {$this->navn}\n");
        $liste = array_map(fn($x) => $x ** 2, [1, 2, 3]);
        return match (true) { $r[0] > 0 => G * $this->masse / $r[0], default => 0 };
    }
}

echo "Antall: " . Planet::$antall, PHP_EOL, sprintf('%05.2f', 3.14159);
