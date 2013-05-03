jbclipy
=======

##Description
Automation and simplification scripting for managing JBoss AS7/EAP6 instances

##Examples
This section has some basic examples

###Datasource Management
Datasources are easy to manage.

    import os
    if 'JBOSS_HOME' not in os.environ:
	    print "Environment Variable: JBOSS_HOME must be defined"
        exit(-1)

    import jbclipy

    jbcli = jbclipy.JBCliPy()

    #Remove the hypersonic database and driver
    jbcli.remove_h2()

    #Add a driver (ironically the hypersonic one back)
    jbcli.add_jdbc_driver('h2','com.h2database.h2','org.h2.jdbcx.JdbcDataSource')

    #Add a datasource (again, ironically the hypersonic one back)
    jbcli.add_datasource('ExampleDS','java:jboss/datasources/ExampleDS','jdbc:h2:mem:test','h2','sa','sa')

    #Enable the datasource
    jbcli.enable_datasource('ExampleDS')

    #Test the datasource connection
    jbcli.test_datasource('ExampleDS')

    #Print execution string for veification
    jbcli.print_execution()

    #Execute the commands
    jbcli.execute()


###Profile Transforms
It is easier to slim a profile versus adding new subsystems.

####standalone-full-ha.xml to standalone.xml

This example slims the standalone-full-ha.xml to standalone.xml. Simply start your JBoss instance using the standalone-full-ha.xml profile (MAKE SURE TO BACK UP THIS FILE FIRST) then run the following script

    import os
    if 'JBOSS_HOME' not in os.environ:
	    print "Environment Variable: JBOSS_HOME must be defined"
        exit(-1)


    import jbclipy

    # Create a JBMod instance
    jbcli = jbclipy.JBCliPy()

    # Build a solution
    # This particular solution slims standalone-full-ha.xml to standalone.xml
    jbcli.remove_clustering()
    jbcli.remove_messaging()
    jbcli.remove_cmp()
    jbcli.remove_jacorb()
    jbcli.remove_jaxr()
    jbcli.remove_jsr77()
    jbcli.add_console_handler('CONSOLE')
    jbcli.add_handler_to_root_logger('CONSOLE')

    # Print the execution string for reference
    jbcli.print_execution()

    # Execute the commands
    jbcli.execute()
