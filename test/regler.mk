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
