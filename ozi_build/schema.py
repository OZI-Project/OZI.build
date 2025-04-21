VALID_PROJECT = {
    "authors": {"description": """A list of mappings with keys 'name' and 'email'."""},
    "classifiers": {
        "description": """A list of [classifiers](https://pypi.python.org/pypi?%3Aaction=list_classifiers)."""
    },
    "dependencies": {"description": """A list of requirements."""},
    "description": {
        "description": """A short project summary."""
    },
    "dynamic": {
        "description": """A list of other headers to be treated as dynamic fields."""
    },
    "entry-points": {"description": """A collection of tables. Each sub-table name is an entry point group."""},
    "gui-scripts": {"description": """A table of entry point names mapped to modules."""},
    "keywords": {"description": """Comma-separated keywords as a string."""},
    "license": {
        "description": """Text indicating the license covering the distribution.
This text can be either a valid license expression as defined in [pep639](https://www.python.org/dev/peps/pep-0639/#id88) or any free text.
"""
    },
    "license-files": {"description": """An array of license filenames."""},
    "maintainers": {"description": """A collection of tables with keys 'name' and 'email'."""},
    "name": {"description": """The non-normalized package name."""},
    "optional-dependencies": {"description": "A mapping of optional dependency group names to lists of requirements."},
    "readme": {"description": "A string of the readme filename or a table with keys ``file`` and ``content-type``."},
    "requires-python": {
        "description": """A version specifier for the versions of Python this requires, e.g. ``~=3.3`` or
``>=3.3,<4`` which are equivalents."""
    },
    "scripts": {"description": """A table of entry point names mapped to modules."""},
    "urls": {
        "description": """A table of labels mapped to urls.
For example:

``` toml
[project.urls]
Source = "https://github.com/OZI-Project/OZI.build"
```
"""
    },
    "version": {"description": """The current package version."""},
}

VALID_OPTIONS = {
    "author": {"description": """:::{deprecated} 1.15.0:::
               Your name"""},
    "author-email": {
        "description": """:::{deprecated} 1.15.0:::
Your email address

e.g. for ozi-build itself:

``` toml
[tool.ozi-build.metadata]
author="Thibault Saunier"
author-email="tsaunier@gnome.org"
```"""
    },
    "classifiers": {
        "description": """:::{deprecated} 1.15.0:::
A list of [classifiers](https://pypi.python.org/pypi?%3Aaction=list_classifiers)."""
    },
    "description": {
        "description": """:::{deprecated} 1.15.0:::
The description of the project as a string if you do not want to specify 'description-file'"""
    },
    "description-file": {
        "description": """:::{deprecated} 1.15.0:::
A path (relative to the .toml file) to a file containing a longer description
of your package to show on PyPI. This should be written in reStructuredText
  Markdown or plain text, and the filename should have the appropriate extension
  (`.rst`, `.md` or `.txt`)."""
    },
    "home-page": {
        "description": """:::{deprecated} 1.12.0:::
A string containing the URL for the package's home page.

Example:

`http://www.example.com/~cschultz/bvote/`"""
    },
    "download-url": {
        "description": """:::{deprecated} 1.12.0:::
A string containing the URL for the package's source, will replace '{version}' with the current version."""
    },
    "dynamic": {
        "description": """:::{deprecated} 1.15.0:::
A list of other headers to be treated as dynamic fields."""
    },
    "keywords": {"description": """:::{deprecated} 1.15.0:::
Comma-separated keywords as a string."""},
    "license": {
        "description": """:::{deprecated} 1.15.0:::
Text indicating the license covering the distribution. This text can be either a valid license expression as defined in [pep639](https://www.python.org/dev/peps/pep-0639/#id88) or any free text."""
    },
    "license-expression": {"description": """:::{deprecated} 1.15.0:::
A SPDX license expression."""},
    "license-file": {"description": """:::{deprecated} 1.15.0:::
The license filename."""},
    "maintainer": {
        "description": """:::{deprecated} 1.15.0:::
Name of current maintainer of the project (if different from author)"""
    },
    "maintainer-email": {
        "description": """:::{deprecated} 1.15.0:::
Maintainer email address

Example:

``` toml
[tool.ozi-build.metadata]
maintainer="Robin Goode"
maintainer-email="rgoode@example.org"
```"""
    },
    "meson-options": {
        "description": """A list of default meson options to set, can be overriden and expended through the `MESON_ARGS`
environement variable at build time."""
    },
    "meson-python-option-name": {
        "description": """The name of the meson options that is used in the meson build definition
to set the python installation when using
[`python.find_installation()`](http://mesonbuild.com/Python-module.html#find_installation)."""
    },
    "module": {
        "description": """:::{deprecated} 1.15.0:::
The name of the module, will use the meson project name if not specified"""
    },
    "obsoletes": {
        "description": """
A list of PyPI packages that this project should not be installed concurrently with.

``` toml
      obsoletes = [
        "OtherProject",
        "AnotherProject==3.4",
        'virtual_package; python_version >= "3.4"',
      ]
```
"""
    },
    "pkg-info-file": {
        "description": """Pass a PKG-INFO file direcly usable.

> ! NOTE: All other keys will be ignored if you pass an already prepared `PKG-INFO`
> file
"""
    },
    "platforms": {"description": "Supported Python platforms, can be 'any', py3, etc..."},
    "project-urls": {
        "description": """:::{deprecated} 1.15.0:::
A list of `Type, url` as described in the
[pep345](https://www.python.org/dev/peps/pep-0345/#project-url-multiple-use).
For example:

``` toml
project-urls = [
    "Source, https://gitlab.com/OZI-Project/OZI.build",
]
```"""
    },
    "provides": {
        "description": """A list of PyPI packages that this project provides its own version of.

``` toml
      provides = [
        "OtherProject",
        "AnotherProject==3.4",
        'virtual_package; python_version >= "3.4"',
      ]
```"""
    },
    "pure-python-abi": {
        "description": """An override of the pure python abi build target e.g. ``py3-none``."""
    },
    "requires": {
        "description": """:::{deprecated} 1.3.0
Use project.dependencies instead.
:::
A list of other packages from PyPI that this package needs. Each package may
be followed by a version specifier like ``(>=4.1)`` or ``>=4.1``, and/or an
[environment marker](https://www.python.org/dev/peps/pep-0345/#environment-markers)
after a semicolon. For example:

``` toml
      requires = [
          "requests >=2.6",
          "configparser; python_version == '2.7'",
      ]
```"""
    },
    "requires-external": {
        "description": """A list of non-PyPI dependency packages. For example:

``` toml
      requires-external = [
          "git",
          "node",
      ]
```"""
    },
    "requires-python": {
        "description": """:::{deprecated} 1.15.0:::
A version specifier for the versions of Python this requires, e.g. ``~=3.3`` or
``>=3.3,<4`` which are equivalents."""
    },
    "summary": {
        "description": """:::{deprecated} 1.15.0:::
A one sentence summary about the package""",
    },
}
VALID_PYC_WHEEL_OPTIONS = {
    'exclude': {'description': 'A regular expression of files for pyc_wheel to ignore.'},
    'quiet': {'description': 'Quiet non-error output of pyc_wheel.'},
}
