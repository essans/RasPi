Creation of this documentation
==============================

In creating a set of recipes for use on the raspberry-pi my goal is to document things along the way.   Something which I already do: Setting up a new computer, noting down a new piece of code, or script for future use, or a technique for solving a problem. 

I am a voracious note taker, whether it is handwritten in a notebook (I'm a big fan of the `Barron Fig <http://www.barronfig.com/>`_ Vanguard softcover notebooks - always dot grid), and I use a combination of Evernote and private github repositories.

For my raspberry-pi projects I want to experiment with documenting things on the web.  I started with a collection of markdown and code pages in a public github repository but it's difficult to keep organized and make available in a form that is usable for the purpose in mind.  

I've always likeed the "read the docs" theme for technical documentation and my thinking is that maybe it will work for documenting what I now call a collection of recipes for the raspberry-pi.  

This section documents how I'm going about doing this.  A recipe in and of itself.


Prerequisites
-------------
* raspberry-pi
* github.com account and repository
* readthedocs.org account created/linked using your github login.

Github Repository
-----------------
The github repository can either have existing code/documents, or can be a freshly created one.  We are going to create a separate docs folder later.


Raspberry pi set-up
-------------------
It doesn't have to be a raspberry pi, but I've used one here.

(1) Check to see that ``git`` is installed with ``git --version``.  If can be installed with:

.. code-block:: bash
   :linenos:

   sudo apt-get update
   sudo apt-get install git


Now configure:

.. code-block:: bash
   :linenos:

   git config --global user.email "address@domain.com"    
   git config --global user.name "First Last"


(2) Install a couple of packages needed to build the docs:

.. code-block:: bash
   :linenos:

   sudo pip3 install sphinx
   sudo pip3 install sphinx-rtd-theme
   sudo pip3 install recommonmark

``sphinx`` is a documentation generator on which I did some research on the web.   I also used this getting started guide `here <https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html>_`.  I use this in the following with a few minor changes.

``sphinx-rtd-theme`` is the theme i want.  There are others.

``recommonmark`` enables the use of .md pages along with the .rst pages that are more commonly used.

(3) In my home directory I keep all the github material in its own subdirectory created with ``mkdir github``.  Now I retrieve the information from github.com repo:

.. code-block:: bash
   :linenos:

   cd github
   git clone https://github.com/essans/RasPi


(4) Set some configurations:

.. code-block:: bash
   :linenos:

   cd RasPi
   
   mkdir docs
   cd docs

   sphinx-quickstart


Once I've filled in the details asked for (which I  can change later) i udpdate the ``conf.py`` file just auto-created.  Most recent conf.py file can be found in the github repo in the ``docs/source`` folder.

(5) Begin creating documentation.
* The "main" file is the ``index.rst`` file found in the ``docs/source`` folder.  It contains text for the start of the docs and lists the other pages in the sequence in which they will be rendered.

* The ``.rst`` extension indicates "Restructured Text (ReST) formatting which is similar to markdown .md mark-up.

* At first glance they both ``.md`` markup and ReST look similar in objectives but with different syntax but it seems that .md is see as a light-weight with ``.rst`` being favoured for use in technical documentation.  Some discussion on this can be found `here. <https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/>`_ 

* I've found a few reference for looking up ``.rst`` syntax including: 
  - https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html#introduction
  - https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

(6) Once the ``index.rst`` and other pages are ready in the ``/docs/source`` folder i then ``cd ..`` up one level and build the documentation by running:

.. code-block:: bash
   :linenos:

   make clean
   make html

There are usually some formatting errors that are flagged and will need to be fixed before running the above and only then proceed to...


(7) Commit and push back to github.com

.. code-block:: bash
   :linenos:

   git add --all
   git commit -m "an initial commit"
   git push -u origin master


(8) Navigate to www.readthedocs.org, login, and go to your projects `dashboard <https://readthedocs.org/dashboard/>`_ and then click on "import a project" button.  Select the repo that should be listed.
