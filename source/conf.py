# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme #import theme

# -- Project information -----------------------------------------------------

project = 'How To Build Doc'
copyright = '2020, Micheal Miao'
author = 'Micheal Miao'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
'sphinx_rtd_theme',#theme
'recommonmark', #markdowm
'sphinxcontrib.plantuml',#plantuml
]

# Specify plantuml command in your conf.py
if sys.platform == 'darwin':# MAC platform
    plantuml = 'java -jar /Users/gmiao/tools/plantuml.jar'


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
latex_engine = 'xelatex'

latex_elements = {
    'papersize': 'a4paper',
    # Additional stuff for the LaTeX preamble.
    'preamble': r'''
    \usepackage{xeCJK}
    \usepackage{indentfirst}
    \setlength{\parindent}{2em}
    \setCJKmainfont[BoldFont=STFangsong, ItalicFont=STKaiti]{STSong}
    \setCJKsansfont[BoldFont=STHeiti]{STXihei}
    \setCJKmonofont{STFangsong}
    ''',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('index', 'How_To_Build_Doc.tex', 'How To Build Doc',
    'author: Michael Miao', 'manual', True),
]

# The master toctree document.
# The document name of the “master” document, that is, the document that contains the root toctree directive.
# Default is 'index'.
# Changed in version 2.0: The default is changed to 'index' from 'contents'.

# If you have your own `conf.py` file, it overrides Read the Doc's default `conf.py`.
# By default, Sphinx expects the master doc to be contents. Read the Docs will set master doc
# to index instead (or whatever it is you have specified in your settings).
# Try adding this to your `conf.py`:

master_doc = 'index'
