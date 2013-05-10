Examples and Recipes
********************
This page provides examples and recipes for using jbclipy effectively

Logging Examples
================
The following examples can be used to configure logging within your application.  

Adding a Console Handler
------------------------
In this example, we look at adding a console handler. A console handler will allow you to log to the console.

.. note::
    The standalone-full-ha.xml profile does not contain a CONSOLE handler by default.

Add the handler::

    import os

    #Make sure JBOSS_HOME is set
    if 'JBOSS_HOME' not in os.environ:
        print 'JBOSS_HOME must be set'
        exit(-1)

    import jbclipy

    # Create an instance
    cli = jbclipy.JBCliPy()

    # Add the console handler CONSOLE
    cli.add_console_handler('CONSOLE',{
        'level' : 'INFO',
        'formatter' : '%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n'
    })

    # Execute
    cli.execute()

Now, you will need to add this console to a logger.  Let's add it to the ROOT logger

Add to root logger::

    cli.add_handler_to_root_logger('CONSOLE')

The end result will have INFO level output printed to the CONSOLE


