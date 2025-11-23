
A simple tool to convert Discourse thread URLs to markdown files.

Discourse threads can get really long and Discourse search is very inconvenient
as it shows only small pieces of the context and just using Ctrl-F doesn't work
as Discourse just showing 20 posts at a time.


Installation:
```sh
pip install git+https://github.com/Andrej730/discourse-md.git

# Or
git clone https://github.com/Andrej730/discourse-md.git
cd discourse-md
pip install -e .
```

Usage:
```sh
discourse-md https://discuss.python.org/t/pep-685-comparison-of-extra-names-for-optional-distribution-dependencies/14141/42 > thread.md
```
