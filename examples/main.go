// Eksempelfil for å se Høst-temaene på Go.
package main

import (
	"errors"
	"fmt"
	"math"
)

const (
	G        = 6.674e-11
	MaksSteg = 10_000
)

type Legeme struct {
	Navn  string
	Masse float64
	X, Y  float64
}

var ErrKollisjon = errors.New("kollisjon")

func (a Legeme) Kraft(b Legeme) (float64, error) {
	r := math.Hypot(b.X-a.X, b.Y-a.Y)
	if r == 0 {
		return 0, fmt.Errorf("%w mellom %s og %s\n", ErrKollisjon, a.Navn, b.Navn)
	}
	return G * a.Masse * b.Masse / (r * r), nil
}

func main() {
	sola := Legeme{Navn: "Sola", Masse: 1.989e30}
	jorda := Legeme{"Jorda", 5.972e24, 1.496e11, 0}
	ferdig := make(chan bool)

	go func() {
		defer close(ferdig)
		for i := 0; i < MaksSteg; i++ {
			if f, err := jorda.Kraft(sola); err == nil {
				fmt.Printf("F = %.3e N, rune = %c\n", f, 'J')
				break
			}
		}
	}()
	<-ferdig
}
