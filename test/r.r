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

# Vanskelige tilfeller: operatorer, formler, egne operatorer, strenger og pipes
`%+%` <- function(a, b) paste0(a, b)
vanskelig <- function(navn = NULL, ..., nøkkel = 1L, blokk = \(x) x * 2) {
  t <- 0; t <- t + 1; t <<- t - 2; t = t * 3 %/% 4 %% 5 ^ 2; t -> u; assign("w", t %o% u)
  lik <- t == 1 || isTRUE(t != 1) && !is.null(navn) | t %in% 1:3 & xor(TRUE, FALSE) && t <= 2 && t >= -1
  tekst <- "a + b == c" %+% 'apostrof \'x\'' %+% r"(rå \n)" %+% sprintf("%s %.2f%%\t\u00e6", navn, 1.5)
  modell <- lm(masse ~ navn + I(navn^2) - 1, data = planeter); koeff <- coef(modell)[["navn"]]
  m <- matrix(1:6, nrow = 2); m[1, ] <- m[2, ] * 2; p <- m %*% t(m); d <- m[m > 2 & m < 6]
  if (nargs() > 1 && ...length() > 0) { args <- list(...); navn <- args[[1]] }
  for (i in seq_len(nrow(m))) { if (i %% 2 == 0) next else if (i > 10) break }
  Person <- setRefClass("Person", fields = list(navn = "character"), methods = list(hei = function() cat(navn, "\n")))
  s <- structure(list(x = 1), class = "legeme"); print.legeme <- function(x, ...) cat("legeme", x$x, "\n")
  resultat <- switch(as.character(t), "0" = -t, "1" = blokk(t), stop("ukjent")); on.exit(rm(u))
  planeter |> subset(masse > 1e24) |> transform(rel = masse / max(masse)) |> with(sum(rel)) + resultat + nchar(tekst)
}
