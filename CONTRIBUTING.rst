.. highlight:: shell

===============================================
Contributing to scikit-surgerybard
===============================================

We welcome contributions to scikit-surgerybard.


Reporting bugs and feature requests
-----------------------------------

Please create a new issue on https://github.com/SciKit-Surgery/scikit-surgerybard/issues/new

When reporting a bug, please include:
* The version of scikit-surgerybard you are using
* Your OS version (for example Windows 10 64-bit, macOS High Sierra, Ubuntu 16.04)
* Detailed steps to reproduce the bug.


Fixing bugs or implement features
---------------------------------

The easiest way to contribute is to follow these guidelines:

1. Look through the issues on https://github.com/SciKit-Surgery/scikit-surgerybard/issues and assign the relevant issue to yourself. If there is not an existing issue that covers your work, please create one: https://github.com/SciKit-Surgery/scikit-surgerybard/issues/new
2. Read the design considerations below.
3. Fork the repository: https://github.com/SciKit-Surgery/scikit-surgerybard/forks/new
4. Create a branch for your changes. The branch name should start with the issue number, followed by hyphen separated words describing the issue. For example: 1-update-contribution-guidelines
5. Make your changes following the coding guidelines below.
6. Commit and push your changes to your fork. The commit message should start with `Issue #<issue number>`, for example: "Issue #1: Fixed typo". Commit in small, related chunks. Review each commit and explain its purpose in the commit message.
7. Submit a merge request: https://github.com/SciKit-Surgery/scikit-surgerybard/merge_requests/new

Design Considerations
---------------------

1. As few dependencies as possible. Try to stick to standard scipy packages like numpy and pandas.
2. Discuss extra dependencies with the team and maybe the outcome will be to create a new separate package, where you can be more specific and more modular.
3. Unit test well, using pytest, with good coverage.
4. All errors as exceptions rather than return codes.


Coding guidelines
-----------------

1. Please follow PEP8 guidelines https://www.python.org/dev/peps/pep-0008/
2. Create a python virtual environment (virtualenv) for development
3. Make sure that pylint passes. You may disable specific warnings within the code where it is reasonable to do so
4. Add unit tests for new and modified code
5. Make sure all existing and new tests pass
6. Make sure all docstrings have been added
7. Make sure all dependencies have been added to requirements
8. Make sure your code works for all required versions of Python
9. Make sure your code works for all required operating systems

