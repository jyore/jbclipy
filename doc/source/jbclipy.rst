API Documentation
*****************
This page details the available methods and uses for jbclipy

.. automodule:: jbclipy

Configuration
+++++++++++++
The Configuration class is to be used for configuring JBoss profiles.  


Constructor
===========
Available constructor

.. autoclass:: Configuration


User Action Methods
===================
These methods provide actions to users to interact with jbclipy

.. automethod:: Configuration.execute
.. automethod:: Configuration.reset
.. automethod:: Configuration.print_execution

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
        
    conf.add_something('name','required1')

            
Supply keyword args to override::
        
    conf.add_something('name','required1',optional1='value',optional_2='value')


Supply a dictionary for overrides::
        
    conf.add_something('name','required1',{
        'optional1':'value',
        'optional-2':'value'
    })

|  

.. automethod:: Configuration.add_extension
.. automethod:: Configuration.add_connector
.. automethod:: Configuration.add_console_handler


Remove Resources
----------------
These methods are used for removing resources

.. automethod:: Configuration.remove_subsystem
.. automethod:: Configuration.remove_extension
.. automethod:: Configuration.remove_socket_binding
.. automethod:: Configuration.remove_connector
.. automethod:: Configuration.remove_console_handler
.. automethod:: Configuration.remove_periodic_rotating_file_handler
.. automethod:: Configuration.remove_size_rotating_file_handler
.. automethod:: Configuration.remove_handler_from_root_logger
.. automethod:: Configuration.remove_jdbc_driver
.. automethod:: Configuration.remove_datasource
.. automethod:: Configuration.remove_xa_datasource
.. automethod:: Configuration.remove_jms_queue
.. automethod:: Configuration.remove_jms_topic


Additional Methods
------------------
Additiona methods that do not fall under Adding or Removing Resources

.. automethod:: Configuration.custom
.. automethod:: Configuration.take_snapshot
.. automethod:: Configuration.delete_snapshot
.. automethod:: Configuration.enable_datasource
.. automethod:: Configuration.disable_datasource
.. automethod:: Configuration.test_datasource
.. automethod:: Configuration.enable_xa_datasource
.. automethod:: Configuration.disable_xa_datasource
.. automethod:: Configuration.test_xa_datasource



Bulk Methods
============
These methods bundle series of commands together in order to easily perform a task.  An example is the jgroups subsystem. 

In order to completely remove the subsystem, one must make a call to :func:`remove_subsystem`, a call to :func:`remove_extension`, and 5 calls to :func:`remove_socket_binding`.  This can be tedious for a user to do, so the bulk method :func:`remove_jgroups` is provided to perform all of the actions needed in order to remove the jgroups subsystem.


.. automethod:: Configuration.remove_jgroups
.. automethod:: Configuration.remove_modcluster
.. automethod:: Configuration.remove_clustering
.. automethod:: Configuration.add_ajp_connector
.. automethod:: Configuration.remove_messaging
.. automethod:: Configuration.remove_mail
.. automethod:: Configuration.remove_cmp
.. automethod:: Configuration.remove_jacorb
.. automethod:: Configuration.remove_jaxr
.. automethod:: Configuration.remove_jsr77
.. automethod:: Configuration.remove_h2


Runtime
+++++++
The Runtime class is used to get and set runtime information in JBoss.


Utility Functions
+++++++++++++++++
Utility functions are available to help make certain configurations easier.

.. autofunction:: make_filter



