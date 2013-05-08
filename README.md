jbclipy
=======

##Description
Automation and simplification scripting for managing JBoss AS7/EAP6 instances

##Examples
This section has some basic examples

###Working with Base Configs
You can grab a working dictionary to work with for any resource addition.  This base config dictionary will provide you with all options available to pass into the creation of the resource.  

Inside a base config, any possible defaults are inserted already, required options without defaults are empty strings, and non-required options are left at None.  When passing the dictionary to a add resource method, any option that is `None` will be ignored

Here is an example of a base config:

    Python Shell
    >>> import jbclipy
    >>> jbcli = jbclipy.JBCliPy()
    >>> jbcli.get_base_config('console-handler')
    {'filter': None, 'target': None, 'encoding': None, 'level': 'INFO', 'autoflush': None, 'formatter': '%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n'}


As you can see, the basic required options are populate with defaults.  But let's say we want to add `autoflush=true` and change the log level to `level=DEBUG`.  We can easily do this by using a dictionary copy in python.

	Python Shell
    >>> import jbclipy
    >>> jbcli = jbclipy.JBCliPy()
    >>> dict(jbcli.get_base_config('console-handler'), **{
    ...    'level' : 'DEBUG',
    ...    'autoflush' : 'true'
    ...})
    {'filter': None, 'autoflush': 'true', 'formatter': '%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n', 'target': None, 'encoding': None, 'level': 'DEBUG'}


Using the dictionary copy with two dictionaries, we take the base config dictionary then update its keys with our supplied dictionary.  You can see base config dictionary values are all in place, but with the two updates supplied. 

Using base configs with a dictionary copy to update your parameters is a great way to get any and all base configurations required to add resources and customize them with your own settings.  

###Datasource Management
Datasources are easy to manage.

    import os
    if 'JBOSS_HOME' not in os.environ:
        print "Environment Variable: JBOSS_HOME must be defined"
        exit(-1)

    import jbclipy

    # Create a JBCliPy instance
    jbcli = jbclipy.JBCliPy()

    #Remove the hypersonic database and driver
    jbcli.remove_h2()

    #Add a driver (ironically the hypersonic one back)
    jbcli.add_jdbc_driver('h2', {
        'driver-module-name'              : 'com.h2database.h2',
        'driver-xa-datasource-class-name' : 'org.h2.jdbcx.JdbcDataSource'
    })

    #Add a datasource (again, ironically the hypersonic one back)  
    jbcli.add_datasource('ExampleDS', {
        'jndi-name'        : 'java:jboss/datasources/ExampleDS',
        'connection-url'   : 'jdbc:h2:mem:test;DB_CLOSE_DELAY=-1',
        'driver-name'      : 'h2',
        'user-name'        : 'sa',
        'password'         : 'sa',
        'use-java-context' : 'true'
    })

    #Enable the datasource
    jbcli.enable_datasource('ExampleDS')

    #Print execution string for veification
    jbcli.print_execution()

    #Execute the commands
    jbcli.execute()


###Profile Transforms
It is easier to slim a profile versus adding new subsystems.

####standalone-full-ha.xml to standalone.xml

This example slims the standalone-full-ha.xml to standalone.xml. Simply start your JBoss instance using the standalone-full-ha.xml profile then run the following script

    import os
    if 'JBOSS_HOME' not in os.environ:
        print "Environment Variable: JBOSS_HOME must be defined"
        exit(-1)


    import jbclipy

    # Create a JBCliPy instance
    jbcli = jbclipy.JBCliPy()

    # Snapshot the current solution in case you need to revert
    jbcli.take_snapshot()

    # Build a solution
    # This particular solution slims standalone-full-ha.xml to standalone.xml
    jbcli.remove_clustering()
    jbcli.remove_messaging()
    jbcli.remove_cmp()
    jbcli.remove_jacorb()
    jbcli.remove_jaxr()
    jbcli.remove_jsr77()
    jbcli.add_console_handler('CONSOLE', jbcli.get_base_config('console-handler'))
    jbcli.add_handler_to_root_logger('CONSOLE')

    # Print the execution string for reference
    jbcli.print_execution()

    # Execute the commands
    jbcli.execute()
