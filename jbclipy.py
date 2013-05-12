import os,platform,json,subprocess

class Configuration():
    """
    Create a Configuration instance, ready to use with or without authentication

    :param username: If authentication is required, the username to use
    :type username: str
    :param password: If authentication is required, the password to use
    :type password: str



    **No authentication example**

    >>> import jbclipy
    >>> conf = jbclipy.Configuration()
    >>> conf.print_execution()
    jboss-cli.sh -c --commands=batch,<commands>,run-batch

    **Authentication example**

    >>> import jbclipy
    >>> conf = jbclipy.Configuration("username","password")
    >>> conf.print_execution()
    jboss-cli.sh -c --user=username --password=password --commands=batch,<commands>,run-batch

    .. Note::

        On Windows, jbclipy will automatically be configured to use `jboss-cli.bat`

    |  
    """
    #Constructor
    def __init__(self,username=None,password=None):
        
        if platform.system() == 'Windows':
            self.connect = [os.environ["JBOSS_HOME"] + '/bin/jboss-cli.bat', '-c']
        else:
            self.connect = [os.environ["JBOSS_HOME"] + '/bin/jboss-cli.sh', '-c']

        if username and password:
            self.connect.append('--user=%s' % username)
            self.connect.append('--password=%s' % password)
            
        self.commands = []

    def _dict2params(self,dictionary):
        """
        Private method to conver dictionaries to parameter strings
        |  
        """
        s = ''
        for key in dictionary:
            if dictionary[key] == None:
                pass  
            elif isinstance(dictionary[key],dict):
                s = s + ',' + key + '=%s' + json.dumps(dictionary[key],separators=(',','=>'))
            elif isinstance(dictionary[key],list):
                if len(dictionary[key]) > 0:
                    s = s + ',' + key.replace('_','-') + '=["%s"]' % '","'.join(item for item in dictionary[key])
                else:
                    pass
            else:
                s = s + ',' + key + '="%s"' % dictionary[key]
        return s


    # User Actions
    def execute(self):
        """
        Call to execute commands batch
        
        |  
        """
        if platform.system() == 'Windows':
            name = r'C:\WINDOWS\TEMP\execute.cli'
        else:
            name = r'/tmp/execute.cli'

        fh = open(name,'w')

        fh.write('batch\n%s\nrun-batch' % '\n'.join(self.commands))
        fh.close()

        subprocess.call(self.connect + ['--file='+name]) 
        os.remove(name)
        self.reset()

    def reset(self):
        """
        Removes all commands in the batch
        
        |  
        """
        self.commands = []

    def print_execution(self):
        """
        Prints the execution string
        
        |  
        """
        print(' '.join(self.connect + ['--commands=batch,%s,run-batch' % ','.join(self.commands)]))

    #Build Methods
    def custom(self,cmd):
        """
        Allows a user to add a custom command to the command list
        
        :param cmd: The command to add for execution
        :type cmd: str
        
        |  
        """
        self.commands.append(cmd)

    def _add_resource(self,base,params):
        """
        Private helper method to build command strings
        
        |  
        """
        if isinstance(params,dict):
            self.commands.append((base + self._dict2params(params) + ')').replace('(,','('))
        else:
            raise TypeError('Input [params] type should be a dictionary')
        
    def remove_subsystem(self,subsystem):
        """
        Removes a subsystem from JBoss

        :param subsystem: The name of the subsystem to remove
        :type subsystem: str

        Example of removing the modcluster subsystem::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('modcluster')
            conf.execute()

        .. warning::
            You should call :func:`remove_extension` in addition to removing the subsystem
            
        |  
        """
        self.commands.append('/subsystem=%s:remove()' % subsystem)

    def add_extension(self,extension):
        """
        Adds an extension to JBoss

        :param extension: The name of the extension to add
        :type extension: str

        Example of adding the modcluster extension::

            conf = jbclipy.Configuration()
            conf.add_extension('org.jboss.as.modcluster')
            conf.execute()
            
        .. note::
            You should make sure that a subsystem is present before calling :func:`add_extension`
            
        |  
        """
        self.commands.append('/extension=%s:add()' % extension)
        
    def remove_extension(self,extension):
        """
        Removes an extension from JBoss

        :param extension: The name of the extension to remove
        :type extension: str

        Example of removing the modcluster extension::

            conf = jbclipy.Configuration()
            conf.remove_extension('modcluster')
            conf.execute()
            
        .. warning::
            You should call :func:`remove_subsystem` before calling :func:`remove_extension`
            
        |  
        """
        self.commands.append('/extension=%s:remove()' % extension)

    def add_socket_binding(self):
        raise NotImplementedError('This method will be available at a future date')

    def remove_socket_binding(self,binding):
        """
        Removes a socket binding

        :param binding: Name of the socket-binding to remove
        :type bindind: str

        .. warning::
            You should only remove a socket binding that is not being referenced in any subsystems
            
        |  
        """
        self.commands.append('/socket-binding-group=standard-sockets/socket-binding=%s:remove()' % binding)

    def add_connector(self,name,protocol,scheme,socket_binding,*args,**kwargs):
        """
        Add a connector

        :param name: The name of the connector
        :type name: str
        :param protocol: The protocol to use
        :type protocol: str
        :param scheme: The scheme to direct traffic under
        :type scheme: str
        :param socket_binding: The name of the socket binding to use for traffic
        :type socket_binding: str
        :param args: An optional dictionary with default overrides
        :type args: dict
        :param kwargs: Instead of a dict, supply keyword args for optional parameters
        :type kwargs: various
        :raises: TypeError

        |

        **Optional Parameters:**
        
        +----------------+--------+-------------------------+-------------------------+
        | Parameter Name |  Type  |         Default         |          Example        |
        +================+========+=========================+=========================+
        | enable-lookups |  str   |          None           |          'true'         |
        +----------------+--------+-------------------------+-------------------------+
        | max-connections|  str   |          None           |          '512'          |
        +----------------+--------+-------------------------+-------------------------+
        | proxy-port     |  str   |          None           |          '1234'         |
        +----------------+--------+-------------------------+-------------------------+
        | secure         |  str   |          None           |          'true'         |
        +----------------+--------+-------------------------+-------------------------+
        | enabled        |  str   |          None           |          'true'         |
        +----------------+--------+-------------------------+-------------------------+
        | redirect-port  |  str   |          None           |          '1234'         |
        +----------------+--------+-------------------------+-------------------------+
        | executor       |  str   |          None           |       'myExecutor'      |
        +----------------+--------+-------------------------+-------------------------+
        | max-post-size  |  str   |          None           |        '2097152'        |
        +----------------+--------+-------------------------+-------------------------+
        | max-save-post- |        |                         |                         |
        | size           |  str   |          None           |         '4096'          |
        +----------------+--------+-------------------------+-------------------------+
        | proxy-name     |  str   |          None           |        'myProxy'        |
        +----------------+--------+-------------------------+-------------------------+
        | virtual-server |  list  |          None           |  ['server1','server2']  |
        +----------------+--------+-------------------------+-------------------------+
            
        |  
        """
        params = {'protocol':protocol,'scheme':scheme,'socket-binding':socket_binding}

        if len(args):
            if isinstance(args[0],dict):
                params.update(args[0])
            else:
                raise TypeError('argument must be a dictionary')
        else:
            params.update(kwargs)
        
        self._add_resource('/subsystem=web/connector=%s:add(name="%s"' % (name,name),params)

    def remove_connector(self,name):
        """
        Removes a connector

        :param name: Name of the connector to remove
        :type name: str
        
        |  
        """
        self.commands.append('/subsystem=web/connector=%s:remove()' % name)

    def add_console_handler(self,name,*args,**kwargs):
        """
        Add a console handler

        :param name: A name for the console handler
        :type name: str
        :param args: An optional dictionary with default overrides
        :type args: dict
        :param kwargs: Instead of a dict, supply keyword args for optional parameters
        :type kwargs: various
        :raises: TypeError

        |

        **Optional Parameters:**
        
        +----------------+--------+-------------------------+-------------------------+
        | Parameter Name |  Type  |         Default         |          Example        |
        +================+========+=========================+=========================+
        | level          |  str   |         'INFO'          |          'DEBUG'        |
        +----------------+--------+-------------------------+-------------------------+
        | formatter      |  str   | '%d{HH:mm:ss,SSS}       | '%d{HH:mm:ss,SSS}       |
        |                |        | %-5p [%c] (%t) %s%E%n'  | %-5p [%c] (%t) %s%E%n'  |
        +----------------+--------+-------------------------+-------------------------+
        | autoflush      |  str   |          None           |          'true'         |
        +----------------+--------+-------------------------+-------------------------+
        | encoding       |  str   |          None           |          'UTF-8'        |
        +----------------+--------+-------------------------+-------------------------+
        | filter         |  dict  |          None           | See :func:`make_filter` |
        +----------------+--------+-------------------------+-------------------------+
        | target         |  str   |       'System.out'      |       'Systen.err'      |
        +----------------+--------+-------------------------+-------------------------+
            
        |  
        """
        params = {
            'level':'INFO',
            'formatter':'%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n',
            'target':'System.out'
        }

        if len(args):
            if isinstance(args[0],dict):
                params.update(args[0])
            else:
                raise TypeError('argument must be a dictionary')
        else:
            params.update(kwargs)

        self._add_resource('/subsystem=logging/console-handler=%s:add(name="%s"' % (name,name),params)

    def remove_console_handler(self,name):
        """
        Removes a console handler

        :param name: Name of the console handler to remove
        :type name: str

        .. warning::
            You must make sure the handler is not part of a logger or root logger to remove
            
        |  
        """
        self.commands.append('/subsystem=logging/console-handler=%s:remove()' % name)

    def add_periodic_rotating_file_handler(self,name,params):
        self._add_resource('/subsystem=logging/periodic_rotating_file_handler=%s:add(name="%s"' % (name,name),params)

    def remove_periodic_rotating_file_handler(self,name):
        """
        Removes a periodic rotating file handler

        :param name: Name of the periodic rotating file handler to remove
        :type name: str

        .. warning::
            You must make sure the handler is not part of a logger or root logger to remove
            
        |  
        """
        self.commands.append('/subsystem=logging/periodic_rotating_file_handler=%s:remove()' % name)

    def add_size_rotating_file_handler(self,name,params):
        self._add_resource('/subsystem=logging/size_rotating_file_handler=%s:add(name="%s",',params)

    def remove_size_rotating_file_handler(self,name):
        """
        Removes a size rotating file handler

        :param name: Name of the size rotating file handler to remove
        :type name: str

        .. warning::
            You must make sure the handler is not part of a logger or root logger to remove
            
        |  
        """
        self.commands.append('/subsystem=logging/size_rotating_file_handler=%s:remove()' % name)

    def add_logger(self,name,params):
        self._add_resource('/subsystem=logging/logger=%s:add(' % name,params)

    def add_handler_to_root_logger(self,name):
        self.commands.append('/subsystem=logging/root-logger=ROOT:root-logger-assign-handler(name="%s")' % name)

    def remove_handler_from_root_logger(self,name):
        """
        Removes a handler from the root logger

        :param name: Name of the handler reference to remove
        :type name: str,bool
        
        |  
        """
        self.commands.append('/subsystem=logging/root-logger=ROOT:root-logger-unassign-handler(name="%s")' % name)

    def add_jdbc_driver(self,name,params):
        self._add_resource('/subsystem=datasources/jdbc-driver=%s:add(driver-name="%s"' % (name,name),params)
        
    def remove_jdbc_driver(self,name):
        """
        Removes a jdbc driver

        :param name: Name of the driver to remove
        :type name: str

        .. warning::
            You must remove any datasources using the driver before the driver can be removed.
            See :func:`remove_datasource` and :func:`remove_xa_datasource`.
            
        |  
        """
        self.commands.append('/subsystem=datasources/jdbc-driver=%s:remove()' % name)
    
    def add_datasource(self,name,params):
        self._add_resource('/subsystem=datasources/data-source=%s:add(' % (name),params)

    def remove_datasource(self,name):
        """
        Removes a datasource

        :param name: Name of the datasource to remove
        :type name: str
        
        |  
        """
        self.commands.append('/subsystem=datasources/data-source=%s:remove()' % name)

    def enable_datasource(self,name):
        """
        Enables a datasource for application use

        :param name: The name of the datasource to enable
        :type name: str

        .. Note::
            It is a good idea to run this command after :func:`add_datasource`

        |  
        """
        self.commands.append('/subsystem=datasources/data-source=%s:enable()' % name)

    def disable_datasource(self,name):
        """
        Disables a datasource from application use

        :param name: The name of the datasource to disable
        :type name: str

        .. Warning::
            Applications **cannot** use a disabled datasource
            
        |  
        """
        self.commands.append('/subsystem=datasources/data-source=%s:disable()' % name)

    def test_datasource(self,name):
        """
        Tests a datasource's connection

        :param name: The name of the datasource to test
        :type name: str

        |  
        """
        self.commands.append('/subsystem=datasources/data-source=%s:test-connection-in-pool' % name)

    def add_xa_datasource(self,name,params):
        self._add_resource('/subsystem=datasources/xa-data-source=%s:add(' % name, params)

    def remove_xa_datasource(self,name):
        """
        Removes an xa-datasource

        :param name: Name of the xa-datasource to remove
        :type name: str
        
        |  
        """
        self.commands.append('/subsystem=datasources/xa-data-source=%s:remove()' % name)
        
    def enable_xa_datasource(self,name):
        """
        Enables an xa-datasource for application use

        :param name: The name of the xa-datasource to enable
        :type name: str

        .. Note::
            It is a good idea to run this command after :func:`add_xa_datasource`
            
        |  
        """
        self.commands.append('/subsystem=datasources/xa-data-source=%s:enable()' % name)

    def disable_xa_datasource(self,name):
        """
        Disables an xa-datasource from application use

        :param name: The name of the xa-datasource to disable
        :type name: str

        .. Warning::
            Applications **cannot** use a disabled xa-datasource
            
        |  
        """
        self.commands.append('/subsystem=datasources/xa-data-source=%s:disable()' % name)

    def test_xa_datasource(self,name):
        """
        Tests an xa-datasource's connection

        :param name: The name of the xa-datasource to test
        :type name: str

        |  
        """
        self.commands.append('/subsystem=datasources/xa-data-source=%s:test-connection-in-pool' % name)

    #TODO: Convert to dictionary input
    def setup_vault(self,directory,url,password,alias,salt,iteration):
        self.commands.append('/core-service=vault:add(vault-options=[KEYSTORE_URL=%s,KEYSTORE_PASSWORD=%s,KEYSTORE_ALIAS=%s,SALT=%s,ITERATION_COUNT=%s,ENC_FILE_DIR=%s])' % (url,password,alias,salt,iteration,directory))

    def take_snapshot(self):
        """
        Takes a snapshot of the current JBoss profile

        .. Note::
            This is highly recommended to do before adding/removing any resources
            
        |  
        """
        self.commands.append(':take-snapshot')

    def delete_snapshot(self,name):
        """
        Deletes a stored snapshot

        :param name: Name of the snapshot to delete
        :type name: str

        |  
        """
        self.commands.append(':delete-snapshot(name=%s)' % name)

    #TODO: Convert to dictionary input
    def add_jms_queue(self,name,entries,selector=None,durable=None):
        s = '/subsystem=messaging/hornetq-server=default/jms-queue=%s:add(' % name
        if entries:
            s = s + 'entries=["' + '","'.join(entries) + '"]'
        if selector:
            s = s + ',selector=%s' % selector
        if durable:
            s = s + ',durable=%s' % durable

        self.commands.append(s + ')')

    def remove_jms_queue(self,name):
        """
        Removes a JMS Queue

        :param name: Name of the queue to remove
        :type name: str
        
        |  
        """
        self.commands.append('/subsystem=messaging/hornetq-server=default/jms-queue=%s:remove()' % name)

    #TODO: Convert to dictionary input
    def add_jms_topic(self,name,entries):
        s = '/subsystem=messaging/hornetq-server=default/jms-topic=%s:add(' % name
        if entries:
            s = s + 'entries=["' + '","'.join(entries) + '"]'

        self.commands.append(s + ')')

    def remove_jms_topic(self,name):
        """
        Removes a JMS Topic

        :param name: Name of the topic to remove
        :type name: str
        
        |  
        """
        self.commands.append('/subsystem=messaging/hornetq-server=default/jms-topic=%s:remove()' % name)



    """Bulk Methods""" 
    def remove_jgroups(self):
        """
        Removes the jgroups subsystem

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('jgroups')
            conf.remove_extension('org.jboss.as.clustering.jgroups')
            conf.remove_socket_binding('jgroups-mping')
            conf.remove_socket_binding('jgroups-tcp')
            conf.remove_socket_binding('jgroups-tcp-fd')
            conf.remove_socket_binding('jgroups-udp')
            conf.remove_socket_binding('jgroups-udp-fd')
            
        |  
        """
        self.remove_subsystem('jgroups')
        self.remove_extension('org.jboss.as.clustering.jgroups')
        self.remove_socket_binding('jgroups-mping')
        self.remove_socket_binding('jgroups-tcp')
        self.remove_socket_binding('jgroups-tcp-fd')
        self.remove_socket_binding('jgroups-udp')
        self.remove_socket_binding('jgroups-udp-fd')

    def remove_modcluster(self):
        """
        Removes the modcluster subsystem

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('modcluster')
            conf.remove_extension('org.jboss.as.modcluster')
            conf.remove_socket_binding('modcluster')
            
        |  
        """
        self.remove_subsystem('modcluster')
        self.remove_extension('org.jboss.as.modcluster')
        self.remove_socket_binding('modcluster')

    def remove_clustering(self):
        """
        Removes all of Clustering (jgroups + modcluster)

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_jgroups()
            conf.remove_modcluster()
            
        |  
        """
        self.remove_jgroups()
        self.remove_modcluster()

    def add_ajp_connector(self,https=False):
        """
        Adds the AJP Connector

        :param https: Use https if True, http if false
        :type https: bool

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.add_connector('ajp','AJP/1.3','http','ajp')
            # http would be https if https field is true
            
        |  
        """
        self.add_connector('ajp','AJP/1.3','https' if https else 'http','ajp')
        
    def remove_messaging(self):
        """
        Removes the messaging subsystem

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('messaging')
            conf.remove_extension('org.jboss.as.messaging')
            conf.remove_socket_binding('messaging')
            conf.remove_socket_binding('messaging-group')
            conf.remove_socket_binding('messaging-throughput')
            
        |  
        """
        self.remove_subsystem('messaging')
        self.remove_extension('org.jboss.as.messaging')
        self.remove_socket_binding('messaging')
        self.remove_socket_binding('messaging-group')
        self.remove_socket_binding('messaging-throughput')


    def remove_mail(self):
        """
        Removes the mail subsystem

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('mail')
            conf.remove_extension('org.jboss.as.mail')
            conf.custom('/socket-binding-group=standard-sockets/remote-destination-outbound-socket-binding=mail-smtp:remove()')
            
        |  
        """
        self.remove_subsystem('mail')
        self.remove_extension('org.jboss.as.mail')
        self.custom('/socket-binding-group=standard-sockets/remote-destination-outbound-socket-binding=mail-smtp:remove()')

    def remove_cmp(self):
        """
        Removes the cmp subsystem

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('cmp')
            conf.remove_extension('org.jboss.as.cmp')
            
        |  
        """
        self.remove_subsystem('cmp')
        self.remove_extension('org.jboss.as.cmp')

    def remove_jacorb(self):
        """
        Removes the jacorb subsystem

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('jacorb')
            conf.remove_extension('org.jboss.as.jacorb')
            conf.remove_socket_binding('jacorb')
            conf.remove_socket_binding('jacorb-ssl')
            
        |  
        """
        self.remove_subsystem('jacorb')
        self.remove_extension('org.jboss.as.jacorb')
        self.remove_socket_binding('jacorb')
        self.remove_socket_binding('jacorb-ssl')

    def remove_jaxr(self):
        """
        Removes the JAXR subsystem

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('jaxr')
            conf.remove_extension('org.jboss.as.jaxr')
            
        |  
        """
        self.remove_subsystem('jaxr')
        self.remove_extension('org.jboss.as.jaxr')

    def remove_jsr77(self):
        """
        Removes the JSR77 subsystem

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_subsystem('jsr77')
            conf.remove_extension('org.jboss.as.jsr77')
            
        |  
        """
        self.remove_subsystem('jsr77')
        self.remove_extension('org.jboss.as.jsr77')

    def remove_h2(self):
        """
        Removes the Hypersonic database and driver

        Equivalent to::

            conf = jbclipy.Configuration()
            conf.remove_datasource('ExampleDS')
            conf.remove_jdbc_driver('h2')
            
        |  
        """
        self.remove_datasource('ExampleDS')
        self.remove_jdbc_driver('h2')


def make_filter(self):
    """
    Makes a logging filter object

    .. warning::
        Method currently not availabale
        
    :returns: dict
    :raises: NotImplementedError
    """
    raise NotImplementedError('This has not yet been implemented')
