# Makefile for stash
# Uses pd-lib-builder: https://github.com/pure-data/pd-lib-builder

lib.name = stash

# C sources go here later (external tier), e.g.:
# class.sources = src/bank.c

# Vanilla tier: abstractions, help files and docs.
# pd-lib-builder copies these flat into the installed stash/ folder,
# so users can write [stash/bank], [stash/param], ...
datafiles = \
	$(wildcard abstractions/*.pd) \
	$(wildcard help/*.pd) \
	stash-meta.pd \
	README.md \
	LICENSE

PDLIBBUILDER_DIR = .
include $(PDLIBBUILDER_DIR)/Makefile.pdlibbuilder
