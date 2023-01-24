# Web Checker

This is a small Python script I made to easily check for changes on multiple web pages that don't have RSS. It just outputs which lines of code have been removed or added.

## Requirements

* **[requests](https://pypi.org/project/requests/)** - `pip install requests`

## Usage

* Add URL to follow: `python3 webchecker.py +[URL]`
* Remove URL: `python3 webchecker.py -[URL]`
* List followed URLs: `python3 webchecker.py list`
* Check for changes: `python3 webchecker.py`
