ALL_PDFS = \
01-athena.pdf \
01-decaf-spec.pdf \
01-general-info.pdf \
01-project-overview.pdf \
02-scanner-parser-project.pdf \
03-group-signup.pdf \
04-semantics-project.pdf \
05-codegen-project.pdf \
06-dataflow-project.pdf \
07-optimizer-project.pdf

all:	$(ALL_PDFS)

copy: $(COPY_PDFS)
	
%.pdf: %.tex 6035.sty bnf.sty rules-decaf.tex
	latex $<
	latex $< 
	dvips -Ppdf -t letter $*.dvi -o	
	ps2pdf $*.ps
	$(RM) $*.log $*.ps $*.aux $*.dvi

clean:
	$(RM) *.log *.aux $(ALL_PDFS)
        
