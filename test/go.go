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
	kanal, n := make(chan int, 3), 1; n <<= 2; n &^= 1
	go func() { defer close(kanal); for i := range 3 { kanal <- i } }()
	for v := range kanal { fmt.Printf("%s: %v %d\n", jord.Navn, true, v+n) }
}

// Vanskelige tilfeller: operatorer, kanaler, generiske funksjoner, strukturer og strenger
type Tall interface{ ~int | ~float64 }
func Sum[T Tall](verdier ...T) (sum T) { for _, v := range verdier { sum += v }; return }
func (l Legeme) String() string { return fmt.Sprintf("%s (%.2e kg)", l.Navn, l.Masse) }
func vanskelig(inn <-chan int, ut chan<- string) (resultat int, err error) {
	defer func() { if r := recover(); r != nil { err = fmt.Errorf("panikk: %v", r) } }()
	tekst := "a + b == c" + `rå \n streng` + string('æ') + "\t\u00e6"
	bits := 0b1010 | 0x0F&^1 ^ 1<<2; bits >>= 1; bits %= 7; bits &= ^0; resultat = -bits + +bits
	for i, j := 0, 10; i < j && !(i == 5); i, j = i+1, j-1 { resultat += i * j / (j - i) }
	peker := &Legeme{}; *peker = Legeme{Navn: tekst}; verdi := *peker; _ = verdi
	switch v := any(peker).(type) { case *Legeme: resultat++; case nil, error: fallthrough; default: _ = v }
	select { case n, ok := <-inn: if ok { resultat += n }; case ut <- "x": ; default: }
	var _ Kraft = (*Legeme)(nil); m := map[string][]int{"a": {1, 2}}; m["a"] = append(m["a"], len(m))
ytre:
	for range 3 { break ytre }
	return Sum(1, 2, 3) + resultat, errors.Join(err, ErrNull)
}
