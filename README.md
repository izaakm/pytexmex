Welcome to `pytexmex`, a Python 3 implementation of `R` package `texmexseq`

Treatment Effect eXplorer for Microbial Ecology eXperiments (texmex)
is designed to normalize OTU count data and
correct for community composition changes that are common to a control and
experimental unit.

- author: Scott Olesen (`swo at mit dot edu`)
- project page: https://almlab.mit.edu/texmex.html
- python github: https://github.com/swo/texmexseq
- R github: https://github.com/swo/texmexseq,
- R CRAN page: http://cran.r-project.org/web/packages/texmexseq/index.html

# Getting started

Read the [documentation](http://pytexmex.readthedocs.io/en/latest/).

Check out the demo script under `demo/`, which uses the demo data in `data/`.

## Installation
I'm not sure the package is fully functional. You can set it up in "development" mode with:

    python3 setup.py develop

After that, you should be able to `import pytexmex` and get everything. If you want to "unlink"
this development version, you can

    python3 setup.py develop --uninstall

# todo
- Check the values I compute against Bulmer's values (i.e., the ones in macroecotools)
- Clean up [documentation](http://www.sphinx-doc.org/en/stable/ext/autodoc.html) (and [this](https://codeandchaos.wordpress.com/2012/07/30/sphinx-autodoc-tutorial-for-dummies/) and [this](http://stackoverflow.com/questions/4616693/automatically-generating-documentation-for-all-python-package-contents))
- Write some nicer documentation [intro](https://wiki.python.org/moin/reStructuredText)
- Make the [package structure](http://docs.python-guide.org/en/latest/writing/structure/) correct
- Make sure the `__init__.py` files are [correct](http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html)
- The `pp_plot_data` is slow because it computes so many pmf's. There's probably a good way to start approximating the values for high `n`.
- Package the poilog functions into a scipy-style distribution
