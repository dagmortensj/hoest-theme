// C: preprosessor, strukturer, pekere og standardbiblioteket
#include <stdio.h>
#include <stdlib.h>
#include "fysikk.h"
#define G 6.674e-11
#define KVADRAT(x) ((x) * (x))
#ifndef MAKS
#  define MAKS 100
#endif

typedef struct {
    char navn[32];
    double masse;
    const int *id;
} Legeme;

enum Farge { ROD, GRONN = 2, BLA };
union Verdi { int i; float f; };
static unsigned long teller = 0UL;
extern volatile int flagg;
/* Kraften mellom to legemer */
double kraft(const Legeme *a, const Legeme *b, double r) {
    return G * a->masse * b->masse / KVADRAT(r);
}

int main(int argc, char *argv[]) {
    Legeme jord = { .navn = "Jorda", .masse = 5.972e24, .id = NULL };
    Legeme *p = malloc(sizeof(Legeme));
    if (p == NULL) return EXIT_FAILURE;
    for (int i = 0; i < MAKS && argv[i] != NULL; i++) { teller += i; }
    printf("%s: %.3e kg, %c, 0x%X\n", jord.navn, jord.masse, 'A', 0xFFu);
    switch (argc) { case 1: break; default: goto slutt; }
slutt:
    free(p);
    return 0;
}

/* Vanskelige tilfeller: pekere, preprosessor, bitoperasjoner og strenger */
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#if defined(DEBUG) && DEBUG > 1
#  warning "feilsøking"
#elif __STDC_VERSION__ >= 201112L
_Static_assert(sizeof(int) == 4, "int");
#endif
typedef double (*kraftfunksjon)(const Legeme *, const Legeme *, double);
static inline int bits(unsigned x) { x &= 0xFFu; x |= 1u << 3; x ^= ~0u; x >>= 2; x <<= 1; return x % 7 != 0; }
void vanskelig(int n, char **argv, int (*sammenlign)(const void *, const void *)) {
    int *p = &n, **pp = &p; n = *p + **pp - -n; n += n-- - --n; n = n == 0 ? -1 : +1;
    const char *s = "a + b == c \"sitat\" \x41\101\n"; char c = '\''; long double ld = 1.5e-3L;
    kraftfunksjon f = kraft; double r = f ? (*f)(NULL, NULL, 1.0) : 0.0; (void) argv;
    struct { unsigned a : 3, b : 5; } felt = { .a = 1, .b = 2 }; felt.a |= felt.b & 3;
    for (size_t i = 0; i < sizeof felt / sizeof(int) && !(n & 1); ++i) n ^= (int) i;
    do { n--; } while (n > 0 && sammenlign != NULL);
    char *tekst = "linje \
fortsatt"; /* kommentar med a + b */ // og enda en, x -= 1
    (void) MAX(s[0], tekst[0]); (void) ld; (void) r; (void) c; (void) bits(1u);
}
