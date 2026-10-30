<?php
// Eksempelfil for å se Høst-temaene på PHP.
declare(strict_types=1);

namespace Fysikk\Bane;

use InvalidArgumentException;

final class Legeme
{
    public const G = 6.674e-11;

    public function __construct(
        public readonly string $navn,
        private float $masse,
        private array $posisjon = [0.0, 0.0],
    ) {}

    public function kraft(Legeme $annet): float
    {
        [$dx, $dy] = [$annet->posisjon[0] - $this->posisjon[0], $annet->posisjon[1] - $this->posisjon[1]];
        $r = sqrt($dx ** 2 + $dy ** 2);
        if ($r === 0.0) {
            throw new InvalidArgumentException("Kollisjon mellom {$this->navn} og {$annet->navn}\n");
        }
        return self::G * $this->masse * $annet->masse / ($r * $r);
    }
}

$sola = new Legeme('Sola', 1.989e30);
foreach (range(1, 3) as $i) {
    echo "Steg $i: {$sola->navn}" . PHP_EOL;
}
