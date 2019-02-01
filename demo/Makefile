.PHONY: all clean

SLIDES=slides

all: ${SLIDES}.pdf

%.pdf: %.tex
	latexmk -pdf $^

clean:
	latexmk -C
	rm -f *.nav *.snm *.bib *.bbl *.run.xml

view: ${SLIDES}.pdf
	xdg-open $^

clean_build: clean all
	latexmk -c
