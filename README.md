# Yahoo Finance Reports
> Use the Yahoo Finance API to get info on stocks of interest and report on them

[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")

[![dependency - requests](https://img.shields.io/badge/dependency-requests-blue)](https://pypi.org/project/requests)


## Yahoo Finance API

For help on using the Yahoo API endpoints, see the SyncWith site's tool:

- https://syncwith.com/api/yahoo-finance/all-endpoints

It lets you build and execute queries in the browser, showing your URLs and sample output.

This project uses the _quote endpoint_ to get detailed info on stocks and the _chart endpoint_ for a timeline of values.


## Installation

Install Python 3 - see [Gist](https://gist.github.com/MichaelCurrin/57caae30bd7b0991098e9804a9494c23).

Create a virtual environment:

```sh
$ python -m venv venv
```

Activate it:

```sh
$ source venv/bin/activate
```

Install packages into it:

```sh
$ make install
```


## Usage

Update [config.py](/app/config.py) for custom stock ticker values. _You have to edit the file directly, but as a follow-up a config file outside of version control will be supported later._

Run the reports:

```sh
$ make run
```

See output CSVs written to [app/var](/app/var).

You can then put those in Google Sheets or Google Data Studio to make your graphs. Or try a Python or JS-based graphing solution.


## License

Licensed under [MIT](/LICENSE) by [MichaelCurrin](https://github.com/MichaelCurrin).
