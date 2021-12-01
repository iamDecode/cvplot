# <img src="https://explaining.ml/images/cvplots/logo.png" height="35"/> Contribution-Value plots

The Contribution-Value plot is a visual encoding for interpreting machine learning models. [[more information]](https://explaining.ml/cvplots)


## Demo

<img src="https://user-images.githubusercontent.com/1223300/132945671-1e7c0b64-fb63-46b3-ac5f-3fa19808242c.png" width="600"/>


## Installation

To install use pip:

```
$ pip install cvplot
```

If you use jupyter lab, also run:

```
$ jupyter labextension install cvplot
```

for classic jupyter notebooks, run:

```
jupyter nbextension install --py --symlink --overwrite --sys-prefix cvplot
jupyter nbextension enable --py --sys-prefix cvplot
```


## Development

For a development installation (requires npm or yarn),

```
$ git clone https://github.com/iamDecode/cvplot.git
$ cd cvplot
```

You may want to (create and) activate a virtual environment before continuing with:

```
$ pip install -e .
$ jupyter labextension install js
$ jupyter nbextension install --py --symlink --overwrite --sys-prefix cvplot
$ jupyter nbextension enable --py --sys-prefix cvplot
```

When actively developing your extension, build Jupyter Lab with the command:

```
$ jupyter lab --watch
```

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.


## Citation

If you want to refer to our visualization, please cite our paper using the following BibTeX entry:

```bibtex
@article{collaris2021comparative,
  title={Comparative Evaluation of Contribution-Value Plots for Machine Learning Understanding},
  author={Collaris, Dennis and van Wijk, Jarke J.},
  journal={Journal of Visualization},
  year={2021},
  issn={1875-8975},
  doi={10.1007/s12650-021-00776-w},
  url={https://doi.org/10.1007/s12650-021-00776-w}
}
```

## License

This project is licensed under the BSD 2-Clause License - see the [LICENSE](LICENSE) file for details.
