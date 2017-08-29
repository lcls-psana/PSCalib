# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = PSCalib-doc
SOURCEDIR     = .
BUILDDIR      = _build
#BUILDDIR      = ../../../PSCalib-doc
GITROOT       = ../..


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)/*


gh-pages:
	cd $(GITROOT) && git checkout --orphan gh-pages && git rm -rf . && mv doc/web/_build/html/* . && rm -rf doc && git add -A && git commit -am "commit new documentation." && @echo "From git repo use command: git push upstream gh-pages -f"

#	cd .. && git checkout --orphan gh-pages && git rm -rf . && touch .nojekyll && mv doc/_build/html/* . && rm -rf doc && git add -A && git commit -am "Makefile is force-commiting new build." && git push upstream gh-pages -f
