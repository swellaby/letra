# Contributing
All contributions are welcomed!


## Developing
All that is needed to work with this repo is [Python][python-download-url] and your favorite editor or IDE, although we recommend [VS Code][vscode-url].

### Setup
To set up your local environment to work on this project:

Clone the repo, change into the directory where you cloned the repo, and then run the bootstrap script
```sh     
git clone https://github.com/swellaby/letra.git
cd letra
pip install -r dev-requirements.txt
```

### Task/Script Runner
This project uses [invoke][invoke-url] to make it easy to run various scripts and tools for common development tasks.

Note that by default invoke tasks can be triggered with either the full `invoke` command, or the shorthand `inv`. The sections below use the `inv` shorthand for brevity.

### Testing
This project uses the [pytest][pytest-url] framework for automated testing.

To execute the test suite, run:
```sh
inv test
# or, shorter-hand
inv t
```

### Linting
This project uses [pycodestyle][pycodestyle-url] for linting and analysis.

pycodestyle can either be invoked directly, or the `invoke` tasks can be leveraged for shorthand.
```sh
inv lint
# or, shorter-hand
inv l
```

### Formatting
This project uses [black][black-url] for automated code formatting.

In order to align with the corresponding guidance from [PEP-8][pep8-url] and cooperate with [pycodestyle][pycodestyle-url], we do utilize a maximum line length of 79 and have updated the `black` configuration accordingly.

To _check_ whether the code is currently formatted correctly, run
```sh
inv check-format
# or, shorter-hand
inv cf
# or
inv fc
```

To _reformat_ all code to comply with the formatting rules, run:
```sh
inv format
# or, shorter-hand
inv f
```

### Submitting changes
Swellaby members can either create a branch within the repository or a branch in their personal fork, make changes in their branch, and then submit a PR. 

Outside contributors should fork the repository, make changes in the fork, and then submit a PR.


[Back to Top][top]

[python-download-url]: https://www.python.org/downloads/
[invoke-url]: http://www.pyinvoke.org/
[vscode-url]: https://code.visualstudio.com/
[pycodestyle-url]: https://pycodestyle.pycqa.org/en/latest/intro.html
[black-url]: https://black.readthedocs.io/en/stable/
[pytest-url]: https://docs.pytest.org/en/stable/
[pep8-url]: https://www.python.org/dev/peps/pep-0008/#maximum-line-length
[top]: CONTRIBUTING.md#contributing
