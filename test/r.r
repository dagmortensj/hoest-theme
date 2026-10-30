# R: vektorer, data frames, funksjoner og pipes
library(dplyr)
library(ggplot2)

G <- 6.674e-11
masser <- c(5.972e24, 6.417e23, 1.898e27)
navn <- c("Jorda", "Mars", "Jupiter")
aktiv <- TRUE; mangler <- NA; tom <- NULL; uendelig <- Inf

kraft <- function(m1, m2, r = 1, ...) {
  if (r <= 0) stop("avstand må være positiv")
  G * m1 * m2 / r^2
}

planeter <- data.frame(navn = navn, masse = masser, stringsAsFactors = FALSE)

tunge <- planeter |>
  filter(masse > 1e24) |>
  mutate(relativ = masse / max(masse)) |>
  arrange(desc(relativ))

for (i in seq_along(masser)) {
  cat(sprintf("%s: %.2e kg\n", navn[i], masser[i]))
}

kvadrat <- \(x) x^2
resultat <- sapply(1:10, kvadrat)
liste <- list(a = 1L, b = "to", c = 3i)
planeter$masse[planeter$navn %in% c("Mars")] <- 0

ggplot(planeter, aes(x = navn, y = masse)) +
  geom_col(fill = "#c4502b") +
  labs(title = "Masser")

while (FALSE) next
repeat { break }
