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
More details coming soon... Run:
```sh
inv test
# or, shorter-hand
inv t
```

### Linting
More details coming soon... Run:
```sh
inv lint
# or, shorter-hand
inv l
```

### Formatting
More details coming soon... Run:
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
[top]: CONTRIBUTING.md#contributing
