Getting Started 
***************
This page details the available methods and uses for jbclipy

Downloading Source
==================

The project can be downloaded using git::

    $ git https://github.com/jyore/jbclipy.git


Building the Docs
=================

If you would like, you can build a local copy of the docs for your personal reference.

First download Sphinx::

    $ sudo easy_install Sphinx

Now, browse to the doc directory and run::

    $ make html

This will build the html files for the documentation. Additionally, you could build a pdf

    $ make latexpdf


Using the Library
=================

You will first want to make sure that JBoss is running with the profile that you would like to manage.

.. note::

    The JBOSS_HOME environment variable should be set

Start JBoss::

    $ cd $JBOSS_HOME/bin
    $ ./standalone.sh -c standalone-full-ha.xml

You can now script a command session to use with jbclipy. In this simple example, we will show how to take a snapshot and then remove the Hypersonic database

**test.py**::

    import os

    #Make sure JBOSS_HOME is set
    if 'JBOSS_HOME' not in os.environ:
        print 'JBOSS_HOME must be set'
        exit(-1)

    import jbclipy

    # Create an instance
    cli = jbclipy.JBCliPy()
    
    # Take a snapshot so we can revert our profile if needed
    cli.take_snapshot()

    # Remove Hypersonic
    cli.remove_h2()

    # Print the command execution string for reference
    cli.print_execution()

    # Execute the commands on JBoss
    cli.execute()

Now, let's run our test::

    $ python test.py
    /path/to/jboss/bin/jboss-cli.sh -c --commands=batch,:take-snapshot,/subsystem=datasources/data-source=ExampleDS:remove(),/subsystem=datasources/jdbc-driver=h2:remove(),run-batch

The commands should execute now.  You should be able to find a snapshot of your profile before the :func:`remove_h2` command was called.  You can check your current profile to ensure that the ExampleDS and the h2 driver were both removed from the project.



