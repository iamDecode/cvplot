cvplot
===============================

Understand machine learning models with Contribution-Value plots

Installation
------------

To install use pip:

    $ pip install cvplot
    $ jupyter nbextension enable --py --sys-prefix cvplot
    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager

To install for jupyterlab

    $ jupyter labextension install cvplot

For a development installation (requires npm),

    $ git clone https://github.com//cvplot.git
    $ cd cvplot
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix cvplot
    $ jupyter nbextension enable --py --sys-prefix cvplot
    $ jupyter labextension install js
    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.

