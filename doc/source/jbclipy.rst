API Documentation
*****************
This page details the available methods and uses for jbclipy

.. automodule:: jbclipy


Constructors
============
Available constructors

.. autoclass:: JBCliPy


User Action Methods
===================
These methods provide actions to users to interact with jbclipy

.. automethod:: JBCliPy.execute
.. automethod:: JBCliPy.reset
.. automethod:: JBCliPy.print_execution

Builder Methods
===============
These methods provide actions to build a command list to send to JBoss, specifically for use in managing the JBoss profile.


Add Resources
-------------
These methods are used for adding resources. A resource can be added using these methods with the following parameter scheme:

* name: The name of the resource to add
* required: Each required option gets its own parameter
* optional: Optional parameters are passed via keyword args or dictionary

.. note::
    Optional parameters with hyphenated names (i.e. proxy-port), when passed as keyword arguments, should be passed using an underscore instead of a hyphen. So the keyword argument for `proxy-port` is `proxy_port`

.. note::
    Some Optional parameters have default values and others have `None`.  `None` values are ignored while the default values will be passed to JBoss.  See the method documentation for a list of optional parameters and their default values.

Use all defaults::
        
    cli.add_something('name','required1')

            
Supply keyword args to override::
        
    cli.add_something('name','required1',optional1='value',optional_2='value')


Supply a dictionary for overrides::
        
    cli.add_something('name','required1',{
        'optional1':'value',
        'optional-2':'value'
    })

|  

.. automethod:: JBCliPy.add_extension
.. automethod:: JBCliPy.add_connector
.. automethod:: JBCliPy.add_console_handler


Remove Resources
----------------
These methods are used for removing resources

.. automethod:: JBCliPy.remove_subsystem
.. automethod:: JBCliPy.remove_extension
.. automethod:: JBCliPy.remove_socket_binding
.. automethod:: JBCliPy.remove_connector
.. automethod:: JBCliPy.remove_console_handler
.. automethod:: JBCliPy.remove_periodic_rotating_file_handler
.. automethod:: JBCliPy.remove_size_rotating_file_handler
.. automethod:: JBCliPy.remove_handler_from_root_logger
.. automethod:: JBCliPy.remove_jdbc_driver
.. automethod:: JBCliPy.remove_datasource
.. automethod:: JBCliPy.remove_xa_datasource
.. automethod:: JBCliPy.remove_jms_queue
.. automethod:: JBCliPy.remove_jms_topic


Additional Methods
------------------
Additiona methods that do not fall under Adding or Removing Resources

.. automethod:: JBCliPy.custom
.. automethod:: JBCliPy.take_snapshot
.. automethod:: JBCliPy.delete_snapshot
.. automethod:: JBCliPy.enable_datasource
.. automethod:: JBCliPy.disable_datasource
.. automethod:: JBCliPy.test_datasource
.. automethod:: JBCliPy.enable_xa_datasource
.. automethod:: JBCliPy.disable_xa_datasource
.. automethod:: JBCliPy.test_xa_datasource



Bulk Methods
============
These methods bundle series of commands together in order to easily perform a task.  An example is the jgroups subsystem. 

In order to completely remove the subsystem, one must make a call to :func:`remove_subsystem`, a call to :func:`remove_extension`, and 5 calls to :func:`remove_socket_binding`.  This can be tedious for a user to do, so the bulk method :func:`remove_jgroups` is provided to perform all of the actions needed in order to remove the jgroups subsystem.


.. automethod:: JBCliPy.remove_jgroups
.. automethod:: JBCliPy.remove_modcluster
.. automethod:: JBCliPy.remove_clustering
.. automethod:: JBCliPy.add_ajp_connector
.. automethod:: JBCliPy.remove_messaging
.. automethod:: JBCliPy.remove_mail
.. automethod:: JBCliPy.remove_cmp
.. automethod:: JBCliPy.remove_jacorb
.. automethod:: JBCliPy.remove_jaxr
.. automethod:: JBCliPy.remove_jsr77
.. automethod:: JBCliPy.remove_h2


Utility Functions
=================

.. autofunction:: make_filter
