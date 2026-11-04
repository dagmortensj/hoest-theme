# Make: variabler, regler, mønstre og funksjoner
.PHONY: alle rydd test
SHELL := /bin/bash
KILDER := $(wildcard */main.tex)
PDFER  := $(KILDER:.tex=.pdf)
PYTHON ?= python3

alle: $(PDFER)

%.pdf: %.tex
	latexmk -lualatex -interaction=nonstopmode $< >/dev/null && echo "OK: $@"

test: alle
	$(PYTHON) -m pytest -q tests/

rydd:
	@rm -f *.aux *.log $(PDFER)

ifeq ($(OS),Windows_NT)
  SKILLE := \\
else
  SKILLE := /
endif

skriv-%:
	@echo "$* = $($*)"

# Vanskelige tilfeller: funksjoner, betingelser, automatiske variabler og flerlinjevariabler
MAPPER := $(sort $(dir $(KILDER)))
FLAGG  += -interaction=nonstopmode -halt-on-error
VERSJON = $(shell git describe --tags 2>/dev/null || echo 0.0.0)
define hjelp
	@echo "Mål: $(filter-out hjelp,$(MAKECMDGOALS))"
	@echo "Versjon: $(VERSJON), $(words $(KILDER)) kilder"
endef
hjelp: ; $(hjelp)
$(PDFER): %.pdf: %.tex $(wildcard %/*.sty) | $(MAPPER)
	$(if $(findstring lualatex,$(FLAGG)),latexmk -lualatex,latexmk -pdf) $(FLAGG) $< >/dev/null 2>&1 && echo "OK: $(@D)"
$(MAPPER):
	@mkdir -p $@
ifneq ($(strip $(PYTHON)),)
  TEST := $(PYTHON) -m pytest $(addprefix tests/,$(notdir $(KILDER:.tex=.py)))
else ifdef CI
  TEST := true
endif
.SUFFIXES: .tex .pdf
.DEFAULT_GOAL := alle
-include lokal.mk
.SECONDEXPANSION:
dyp-%: $$(subst -,/,$$*)/main.tex ; @echo "$* -> $^ ($(patsubst %.tex,%.pdf,$^))"
