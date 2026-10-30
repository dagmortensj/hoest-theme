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
