// Go: pakker, strukturer, grensesnitt, goroutiner og feil
package main

import (
	"errors"
	"fmt"
	m "math"
)

const G = 6.674e-11

type Legeme struct {
	Navn  string  `json:"navn"`
	Masse float64 `json:"masse,omitempty"`
}

type Kraft interface {
	Beregn(a, b *Legeme, r float64) (float64, error)
}

type Liste[T any] []T
var ErrNull = errors.New("avstand er null")

func (l *Legeme) Kraft(annen Legeme, r float64) (float64, error) {
	if r == 0 {
		return 0, ErrNull
	}
	return G * l.Masse * annen.Masse / m.Pow(r, 2), nil
}

func main() {
	jord := &Legeme{Navn: "Jorda", Masse: 5.972e24}
	kanal := make(chan int, 3)
	go func() { defer close(kanal); for i := range 3 { kanal <- i } }()
	for v := range kanal { fmt.Printf("%s: %v %d\n", jord.Navn, true, v) }
}
