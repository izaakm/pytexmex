# Requirements
This is written for Python 3.

# Usage notes
I'm not sure the package is fully functional. You can set it up in "development" mode with:

    python3 setup.py develop

After that, you should be able to `import pytexmex` and get everything. If you want to "unlink"
this development version, you can

    python3 setup.py develop --uninstall

# Documentation
You have to `make` the documentation yourself. Go into `doc` and do, e.g., `make html`. Then the
actual html files will appear in `doc/build/html/index.html`.

# todo
- Check the values I compute against Bulmer's values (i.e., the ones in macroecotools)
- Clean up [documentation](http://www.sphinx-doc.org/en/stable/ext/autodoc.html) (and [this](https://codeandchaos.wordpress.com/2012/07/30/sphinx-autodoc-tutorial-for-dummies/) and [this](http://stackoverflow.com/questions/4616693/automatically-generating-documentation-for-all-python-package-contents))
- Write some nicer documentation [intro](https://wiki.python.org/moin/reStructuredText)
- Put some [equations](http://www.sphinx-doc.org/en/stable/ext/math.html) directly into the documentation
- Make the [package structure](http://docs.python-guide.org/en/latest/writing/structure/) correct
- Make sure the `__init__.py` files are [correct](http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html)
- Write a `requirements.txt`
- Write a `LICENSE`
