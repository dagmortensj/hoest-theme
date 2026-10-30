/* Eksempelfil for å se Høst-temaene på C. */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define G 6.674e-11
#define MAKS_STEG 1000

typedef struct {
    const char *navn;
    double masse;
    double x, y;
} Legeme;

static double avstand(const Legeme *a, const Legeme *b) {
    double dx = b->x - a->x, dy = b->y - a->y;
    return sqrt(dx * dx + dy * dy);
}

int main(int argc, char **argv) {
    Legeme sola = {"Sola", 1.989e30, 0.0, 0.0};
    Legeme jorda = {.navn = "Jorda", .masse = 5.972e24, .x = 1.496e11, .y = 0};
    unsigned int steg = argc > 1 ? (unsigned int) atoi(argv[1]) : MAKS_STEG;

    for (unsigned int i = 0; i < steg; i++) {
        double r = avstand(&sola, &jorda);
        if (r <= 0.0) {
            fprintf(stderr, "Kollisjon etter %u steg\n", i);
            return EXIT_FAILURE;
        }
        double f = G * sola.masse * jorda.masse / (r * r);
        printf("%-6s F = %.3e N\t'%c'\n", jorda.navn, f, 'J');
        break;
    }
    return 0;
}
