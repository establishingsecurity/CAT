.PHONY: INCLUDEPDFS all clean

INCLUDESRCS		:= $(wildcard include/*.tex)
INCLUDEPDFS		:= $(INCLUDESRCS:%.tex=%.pdf)
TEXSRCS			:= $(wildcard *.tex)
DOTSRCS			:= $(wildcard *.dot)

# Artifacts
TEXPDFS			:= $(TEXSRCS:%.tex=%.pdf)
DOTPDFS			:= $(DOTSRCS:%.dot=%.pdf)

# Targets
TEXSVGS			:= $(TEXPDFS:%.pdf=%.svg)
TEXPNGS			:= $(TEXPDFS:%.pdf=%.png)
DOTSVGS			:= $(DOTPDFS:%.pdf=%.svg)
DOTPNGS			:= $(DOTPDFS:%.pdf=%.png)

# Targets
all: $(TEXPDFS) $(TEXSVGS) $(TEXPNGS) $(DOTPDFS) $(DOTSVGS) $(DOTPNGS)

clean:
	rm -rf $(TEXPNGS)
	rm -rf $(TEXSVGS)
	rm -rf $(TEXPDFS)
	rm -rf $(DOTPNGS)
	rm -rf $(DOTSVGS)
	rm -rf $(DOTPDFS)

$(INCLUDEPDFS): %.pdf : %.tex
	echo "Including from $<"

%.pdf: %.tex
	latexmk -pdf "$<"
	latexmk -c

%.pdf: %.dot
	dot -Tpdf "$<" -o "$@"

%.svg: %.pdf
	inkscape -z -f "$^" -l "$@"

%.png: %.pdf
	convert -density 300 "$<" -quality 90 "$@"
