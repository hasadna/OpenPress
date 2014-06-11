Start
=====



Open News is a web app for presenting the news archives.

Open News is written in Python and is open source software released under a BSD license.

Open News is a project of the **Public Knowledge Workshop**, a non-profit organization in Israel dedicated to data transparency in government.


Stack
=====

Server
------

The server is written in Python using **Tornado** (http://www.tornadoweb.org/en/stable/).


Installing Solr
~~~~~~~~~~~~~~~
1. Download latest version @ http://apache.spd.co.il/lucene/solr/
2. Extract the tarball
3. Open a terminal, enter the Example folder
4. Run "java -jar example.jar"
5. Now you can access "http://localhost:8983/solr/" - which is the control panel

Installing pysolr
~~~~~~~~~~~~~~~
0. Verify that pip is installed.
0.1. If pip is not installed follow installation manual here:
http://pip.readthedocs.org/en/latest/installing.html

1. Run the command "pip install pysolr"

Install tornado server
~~~~~~~~~~~~~~~
0. Verify that pip is installed.
0.1. If pip is not installed follow installation manual here:
http://pip.readthedocs.org/en/latest/installing.html

1. Run the command "pip install tornado"


Client
------


System requirements
===================

Open News is been developed on Ubuntu, and should be trivial to deploy to any *nix environment.

Essentially, the project requires an OS equipped with **Python**, **Opencv**, **Git**.


Below we give a basic, opinionated system setup for a number of OSes.

Experienced users may choose to vary from the following instructions.

**IMPORTANT: Ensure you have the minimal system requirements before moving on to install of the project.**


Ubuntu
------

**NOTE:** Use of `sudo` for any command is very dependent on your setup.

Execute the commands without it if you know you don't need it.

Update Your System::

    	sudo apt-get update

Install::

	    sudo apt-get install build-essential cmake pkg-config libgtk2.0-dev python-dev python-numpy
    	sudo pip install virtualenv virtualenvwrapper



if you are planning to work on the OCR then you need open-cv::

        sudo apt-get install libopencv-dev python-opencv opencv-doc


That's all the packages we need for the system, now we need to configure the user's .profile.

Configure::

    # this goes in ~/.profile
    export PYTHONIOENCODING=utf-8
    export WORKON_HOME="/home/{YOUR_USER}/environments"
    export PROJECT_HOME="/home/{YOUR_USER}/projects"
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
    export PIP_USE_MIRRORS=true
    export PIP_INDEX_URL=https://simple.crate.io/


Installing the project
======================

As long as you have met the system requirements above , we're ready to install the project.


Make a virtualenv
-----------------

We are going to setup the project in a new Python virtual environment.

If you are not familiar wth virtualenv or virtualenvwrapper, see the following article:

http://docs.python-guide.org/en/latest/dev/virtualenvs/

We are going to:

* Create a new virtual environment
* Create another directory for our project code
* Make a connection between the two
* Clone the project code into its directory


Ubuntu & Fedora
~~~~~~~~~~~~~~~

Here we go::

    # Create the virtual environment
    mkvirtualenv {PROJECT_NAME}

    # Create a directory for our project code
    mkdir /home/{YOUR_USER}/projects/{PROJECT_NAME}

    # Link our project code directory to our virtual environment
    setvirtualenvproject /home/{YOUR_USER}/environments/{PROJECT_NAME} /home/{YOUR_USER}/projects/{PROJECT_NAME}

    # Move to the root of our project code directory
    cdproject

    # Clone the project
    # Important: Note the "." at the end of the git clone command.
    git clone https://github.com/kobiluria/open-news.git .
