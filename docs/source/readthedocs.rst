Creation of this documentation
==============================
The "read the docs" theme for online documentation is used across the web for `technical documentation <https://bloomberg.github.io/blpapi-docs/python/3.13/blpapi-package.html>`_ and for `lighter weight topics <http://cozmosdk.anki.com/docs/index.html>`_. 

This section documents the documentation creation process.  A recipe in and of itself.


Prerequisites
-------------
* raspberry-pi
* github.com account and repository
* readthedocs.org account created/linked using your github login.


Github Repository
-----------------
The github repository can either have existing code/documents, or can be a freshly created one.  


Raspberry pi set-up
-------------------
It doesn't have to be a raspberry pi, but I've used one here.

First check to see that ``git`` is installed with ``git --version``.  Installed if need be:

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install git


Now configure:

.. code-block:: bash

   git config --global user.email "address@domain.com"    
   git config --global user.name "First Last"


and Install a couple of packages needed to build the docs:

.. code-block:: bash

   sudo pip3 install sphinx
   sudo pip3 install sphinx-rtd-theme
   sudo pip3 install recommonmark

``sphinx`` is a documentation generator that I've seen used in many places.   This is a good "getting started" guide that I used:

   -  `<https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html>`_.  
   
I made some changes along the way, but it was a good place to start.  Lots of trial and error. 

The ``sphinx-rtd-theme`` package is for the theme used for the documentation, and the ``recommonmark`` package enables the use of .md pages along with the .rst pages that are more commonly used.

In my home directory I keep all the github material in its own subdirectory created with ``mkdir github``.  Now I retrieve the information from github.com repo:

.. code-block:: bash

   cd github
   git clone https://github.com/essans/RasPi


Set some configurations:

.. code-block:: bash

   cd RasPi
   
   mkdir docs
   cd docs

   sphinx-quickstart


Once I've filled in the details asked for (which I  can change later) i udpdate the ``conf.py`` file which the ``sphinx-quickstart`` auto-created.  My most recent conf.py file can be found in the github repo in the ``docs/source`` folder.


Begin creating documentation
----------------------------

* The "main" file is the ``index.rst`` file found in the ``docs/source`` folder.  It contains text for the start of the docs and lists the other pages in the sequence in which they will be rendered.

* The ``.rst`` extension indicates "Restructured Text (ReST) formatting which is similar to markdown .md mark-up.

* At first glance they both ``.md`` markup and ReST look similar in objectives but with different syntax but it seems that .md is see as a light-weight with ``.rst`` being favoured for use in technical documentation.  Some discussion on this can be found `here. <https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/>`_ 

* I've found a few reference for looking up ``.rst`` syntax including: 

  - https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html#introduction
  - https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html


Build Docs and push back to github
----------------------------------

Once the ``index.rst`` and other pages are ready in the ``/docs/source`` folder i then ``cd ..`` up one level and build the documentation by running:

.. code-block:: bash

   make clean
   make html

There are usually some formatting errors that are flagged and will need to be fixed before running the above and only then proceed to...


Commit and push back to github.com with:

.. code-block:: bash

   git add --all
   git commit -m "an initial commit"
   git push -u origin master


Import to readthedocs.org
-------------------------
Make any refinements to the docs via github editing and then when ready navigate to www.readthedocs.org, login, and go to the projects `dashboard <https://readthedocs.org/dashboard/>`_ and click on "import a project" button.  Select the repo that should be listed on the dashboard.  

Once built the online docs are visible on https://raspi-recipes.readthedocs.io
