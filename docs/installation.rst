============
Installation
============

Pre-requisites
--------------

Python 3.x and virtualenv

For development
---------------

* Clone from github::

    git clone git@github.com/opullence/python-template.git
    cd python-template/

* Create a virtual environment and install the dev requirements::

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

* Run the tests::

    python -m unittest

For use in another project
--------------------------

Install from github using pip::

    pip install git+ssh://git@github.com/opullence/python-template.git

You can also install a specific commit, branch or tag, for example::

    pip install git+ssh://git@github.com/opullence/python-template.git@0.1.0
