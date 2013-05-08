import os,platform,json,subprocess

class JBCliPy():
    """
    Create a JBClipy Object, ready to use with or without authentication

    :param username: If authentication is required, the username to use
    :type username: str
    :param password: If authentication is required, the password to use
    :type password: str



    **No authentication example**

    >>> cli = jbclipy.JBCliPy()
    >>> print(cli.print_execution())
    jboss-cli.sh -c --commands=batch,<commands>,run-batch

    **Authentication example**

    >>> cli = jbclipy.JBCliPy("username","password")
    >>> print(cli.print_execution())
    jboss-cli.sh -c --user=username --password=password --commands=batch,<commands>,run-batch

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


    _config_bases = {
        'periodic-rotating-file-handler' : {
            'file': {
                'relative-to':'jboss.server.log.dir',
                'path':'default.log'
            }, 
            'formatter':'%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n',
            'level':'INFO',
            'append':'true',
            'suffix':'.yyyy-MM-dd',
            'autoflush':None,
            'encoding':None,
            'filter':None
        },
        'size_-otating-file-handler' : {
            'file': {
                'relative-to':'jboss.server.log.dir',
                'path':'default.log'
            },            
            'rotate_size':'',
            'append':'true',
            'formatter':'%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n',
            'level':'INFO',
            'max_backup_index':None,
            'autoflush':None,
            'encoding':None,
            'filter':None
        },
        'console-handler' : {
            'formatter':'%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n',
            'level':'INFO',
            'autoflush':None,
            'encoding':None,
            'filter':None,
            'target':None
        },
        'logger' : {
            'category':'',
            'filter':'',
            'handlers':[],
            'level':'ALL',
            'use-parent-handlers':''
        },
        'jdbc-driver' : {
            'driver-module-name':'',
            'driver-xa-datasource-class-name':None,
            'deployment-name':None,
            'driver-major-version':None,
            'module-slot':None,
            'driver-class-name':None,
            'driver-minor-version':None,
            'jdbc-compliant':None
        },
        'connector' : {
            'protocol':'',
            'scheme':'',
            'socket-binding':'',
            'enable-lookups':None,
            'max-connections':None,
            'proxy-port':None,
            'secure':None,
            'enabled':None,
            'max-post-size':None,
            'redirect-port':None,
            'executor':None,
            'max-save-post-size':None,
            'proxy-name':None,
            'virtual-server':None
        },
        'datasource' : {
            'jndi-name':'',
            'connection-url':'',
            'driver-name':'',
            'user-name':'',
            'password':'',
            'use-java-context':'true',
            'allocation-retry-wait-millis':None,
            'allocation-retry':None,
            'allow-multiple-users':None,
            'background-validation-millis':None,
            'background-validation':None,
            'blocking-timeout-wait-millis':None,
            'check-valid-connection-sql':None,
            'datasource-class':None,
            'driver-class':None,
            'exception-sorter-class-name':None,
            'exception-sorter-properties':None,
            'flush-strategy':None,
            'idle-timeout-minutes':None,
            'jndi-name':None,
            'jta':None,
            'max-pool-size':None,
            'min-pool-size':None,
            'new-connection-sql':None,
            'pool-prefill':None,
            'pool-use-strict-min':None,
            'prepared-statements-cache-size':None,
            'query-timeout':None,
            'reauth-plugin-class-name':None,
            'reauth-plugin-properties':None,
            'security-domain':None,
            'set-tx-query-timeout':None,
            'share-prepared-statements':None,
            'spy':None,
            'stale-connection-checker-class-name':None,
            'stale-connection-checker-properties':None,
            'track-statements':None,
            'transaction-isolation':None,
            'url-delimiter':None,
            'url-selector-strategy-class-name':None,
            'use-ccm':None,
            'use-fast-fail':None,
            'use-try-lock':None,
            'user-name':None,
            'valid-connection-checker-class-name':None,
            'valid-connection-checker-properties':None,
            'validate-on-match':None
        },
        'xa-datasource' : {
            'jndi-name':'',
            'connection-url':'',
            'driver-name':'',
            'user-name':'',
            'password':'',
            'allocation-retry-wait-millis':None,
            'allocation-retry':None,
            'allow-multiple-users':None,
            'background-validation-millis':None,
            'background-validation':None,
            'blocking-timeout-wait-millis':None,
            'check-valid-connection-sql':None,
            'exception-sorter-class-name':None,
            'exception-sorter-properties':None,
            'flush-strategy':None,
            'idle-timeout-minutes':None,
            'interleaving':None,
            'jta':None,
            'max-pool-size':None,
            'min-pool-size':None,
            'new-connection-sql':None,
            'no-recovery':None,
            'no-tx-separate-pool':None,
            'pad-xid':None,
            'pool-prefill':None,
            'pool-use-strict-min':None,
            'prepared-statements-cache-size':None,
            'query-timeout':None,
            'reauth-plugin-class-name':None,
            'reauth-plugin-properties':None,
            'recovery-password':None,
            'recovery-plugin-class-name':None,
            'recovery-plugin-properties':None,
            'recovery-security-domain':None,
            'recovery-username':None,
            'same-rm-override':None,
            'security-domain':None,
            'set-tx-query-timeout':None,
            'share-prepared-statements':None,
            'spy':None,
            'stale-connection-checker-class-name':None,
            'stale-connection-checker-properties':None,
            'track-statements':None,
            'transaction-isolation':None,
            'url-delimiter':None,
            'url-selector-strategy-class-name':None,
            'use-ccm':None,
            'use-fast-fail':None,
            'use-java-context':'true',
            'use-try-lock':None,
            'user-name':None,
            'valid-connection-checker-class-name':None,
            'valid-connection-checker-properties':None,
            'validate-on-match':None,
            'wrap-xa-resource':None,
            'xa-datasource-class':None,
            'xa-resource-timeout':None
        }
    }

    def _dict2params(self,dictionary):
        s = ''
        for key in dictionary:
            if dictionary[key] == None:
                pass  
            elif isinstance(dictionary[key],dict):
                s = s + ',' + key + '=%s' + json.dumps(dictionary[key],separators=(',','=>'))
            elif isinstance(dictionary[key],list):
                if len(dictionary[key]) > 0:
                    s = s + ',' + key + '=["%s"]' % '","'.join(item for item in dictionary[key])
                else:
                    pass
            else:
                s = s + ',' + key + '="%s"' % dictionary[key]
        return s

    def get_base_config(self,base):
        return self._config_bases[base]

    # User Actions
    def execute(self):
        """
        Call to execute commands batch
        """
        subprocess.call(self.connect + ['--commands=batch,%s,run-batch' % ','.join(self.commands)])
        self.reset()

    def reset(self):
        """
        Removes all commands in the batch
        """
        self.commands = []

    def print_execution(self):
        """
        Prints the execution string
        """
        print(' '.join(self.connect + ['--commands=batch,%s,run-batch' % ','.join(self.commands)]))

    #Build Methods
    def custom(self,cmd):
        """
        Allows a user to add a custom command to the command list
        
        :param cmd: The command to add for execution
        :type cmd: str
        """
        self.commands.append(cmd)

    def _add_resource(self,base,params):
        """
        Private helper method to build command strings
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

            cli = jbclipy.JBCliPy()
            cli.remove_subsystem('modcluster')
            cli.execute()

        .. warning::
            You should call :func:`remove_extension` in addition to removing the subsystem
            
        """
        self.commands.append('/subsystem=%s:remove()' % subsystem)

    def add_extension(self,extension):
        """
        Adds an extension to JBoss

        :param extension: The name of the extension to add
        :type extension: str

        Example of adding the modcluster extension::

            cli = jbclipy.JBCliPy()
            cli.add_extension('modcluster')
            cli.execute()
            
        .. note::
            You should make sure that a subsystem is present before calling :func:`add_extension`
            
        """
        self.commands.append('/extension=%s:add()' % extension)
        
    def remove_extension(self,extension):
        """
        Removes an extension from JBoss

        :param extension: The name of the extension to remove
        :type extension: str

        Example of removing the modcluster extension::

            cli = jbclipy.JBCliPy()
            cli.remove_extension('modcluster')
            cli.execute()
            
        .. warning::
            You should call :func:`remove_subsystem` before calling :func:`remove_extension`
            
        """
        self.commands.append('/extension=%s:remove()' % extension)

    def add_socket_binding(self):
        raise NotImplementedError('This method will be available at a future date')

    def remove_socket_binding(self,binding):
        self.commands.append('/socket-binding-group=standard-sockets/socket-binding=%s:remove()' % binding)

    def add_connector(self,name,params):
        self._add_resource('/subsystem=web/connector=%s:add(name="%s"' % (name,name),params)

    def remove_connector(self,name):
        self.commands.append('/subsystem=web/connector=%s:remove()' % name)

    def add_console_handler(self,name,params):
        self._add_resource('/subsystem=logging/console-handler=%s:add(name="%s"' % (name,name),params)

    def remove_console_handler(self,name):
        self.commands.append('/subsystem=logging/console-handler=%s:remove()' % name)

    def add_periodic_rotating_file_handler(self,name,params):
        self._add_resource('/subsystem=logging/periodic_rotating_file_handler=%s:add(name="%s"' % (name,name),params)

    def remove_periodic_rotating_file_handler(self,name):
        self.commands.append('/subsystem=logging/periodic_rotating_file_handler=%s:remove()' % name)

    def add_size_rotating_file_handler(self,name,params):
        self._add_resource('/subsystem=logging/size_rotating_file_handler=%s:add(name="%s",',params)

    def remove_size_rotating_file_handler(self,name):
        self.commands.append('/subsystem=logging/size_rotating_file_handler=%s:remove()' % name)

    def add_logger(self,name,params):
        self._add_resource('/subsystem=logging/logger=%s:add(' % name,params)

    def add_handler_to_root_logger(self,name):
        self.commands.append('/subsystem=logging/root-logger=ROOT:root-logger-assign-handler(name="%s")' % name)

    def remove_handler_from_root_logger(self,name):
        self.commands.append('/subsystem=logging/root-logger=ROOT:root-logger-unassign-handler(name="%s")' % name)

    def add_jdbc_driver(self,name,params):
        self._add_resource('/subsystem=datasources/jdbc-driver=%s:add(driver-name="%s"' % (name,name),params)
        
    def remove_jdbc_driver(self,name):
        self.commands.append('/subsystem=datasources/jdbc-driver=%s:remove()' % name)
    
    def add_datasource(self,name,params):
        self._add_resource('/subsystem=datasources/data-source=%s:add(' % (name),params)

    def remove_datasource(self,name):
        self.commands.append('/subsystem=datasources/data-source=%s:remove()' % name)

    def enable_datasource(self,name):
        self.commands.append('/subsystem=datasources/data-source=%s:enable()' % name)

    def disable_datasource(self,name):
        self.commands.append('/subsystem=datasources/data-source=%s:disable()' % name)

    def test_datasource(self,name):
        self.commands.append('/subsystem=datasources/data-source=%s:test-connection-in-pool' % name)

    def add_xa_datasource(self,name,params):
        self._add_resource('/subsystem=datasources/xa-data-source=%s:add(' % name, params)

    def remove_xa_datasource(self,name):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:remove()' % name)
        
    def enable_xa_datasource(self,name):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:enable()' % name)

    def disable_xa_datasource(self,name):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:disable()' % name)

    def test_xa_datasource(self,name):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:test-connection-in-pool' % name)

    #TODO: Convert to dictionary input
    def setup_vault(self,directory,url,password,alias,salt,iteration):
        self.commands.append('/core-service=vault:add(vault-options=[KEYSTORE_URL=%s,KEYSTORE_PASSWORD=%s,KEYSTORE_ALIAS=%s,SALT=%s,ITERATION_COUNT=%s,ENC_FILE_DIR=%s])' % (url,password,alias,salt,iteration,directory))

    def take_snapshot(self):
        self.commands.append(':take-snapshot')

    def delete_snapshot(self,name):
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
        self.commands.append('/subsystem=messaging/hornetq-server=default/jms-queue=%s:remove()' % name)

    #TODO: Convert to dictionary input
    def add_jms_topic(self,name,entries):
        s = '/subsystem=messaging/hornetq-server=default/jms-topic=%s:add(' % name
        if entries:
            s = s + 'entries=["' + '","'.join(entries) + '"]'

        self.commands.append(s + ')')

    def remove_jms_topic(self,name):
        self.commands.append('/subsystem=messaging/hornetq-server=default/jms-topic=%s:remove()' % name)



    """Bulk Methods""" 
    def remove_jgroups(self):
        self.remove_subsystem('jgroups')
        self.remove_extension('org.jboss.as.clustering.jgroups')
        self.remove_socket_binding('jgroups-mping')
        self.remove_socket_binding('jgroups-tcp')
        self.remove_socket_binding('jgroups-tcp-fd')
        self.remove_socket_binding('jgroups-udp')
        self.remove_socket_binding('jgroups-udp-fd')

    def remove_modcluster(self):
        self.remove_subsystem('modcluster')
        self.remove_extension('org.jboss.as.modcluster')
        self.remove_socket_binding('modcluster')

    def remove_clustering(self):
        self.remove_jgroups()
        self.remove_modcluster()

    def add_ajp_connector(self,https=False):
        self.add_connector('ajp',dict(self.get_base_config('connector'),**{
            'protocol':'AJP/1.3',
            'scheme':'https' if https else 'http',
            'socket-binding': 'ajp'
        }))
        
    def remove_messaging(self):
        self.remove_subsystem('messaging')
        self.remove_extension('org.jboss.as.messaging')
        self.remove_socket_binding('messaging')
        self.remove_socket_binding('messaging-group')
        self.remove_socket_binding('messaging-throughput')


    def remove_mail(self):
        self.remove_subsystem('mail')
        self.remove_extension('org.jboss.as.mail')
        self.custom('/socket-binding-group=standard-sockets/remote-destination-outbound-socket-binding=mail-smtp:remove()')

    def remove_cmp(self):
        self.remove_subsystem('cmp')
        self.remove_extension('org.jboss.as.cmp')

    def remove_jacorb(self):
        self.remove_subsystem('jacorb')
        self.remove_extension('org.jboss.as.jacorb')
        self.remove_socket_binding('jacorb')
        self.remove_socket_binding('jacorb-ssl')

    def remove_jaxr(self):
        self.remove_subsystem('jaxr')
        self.remove_extension('org.jboss.as.jaxr')

    def remove_jsr77(self):
        self.remove_subsystem('jsr77')
        self.remove_extension('org.jboss.as.jsr77')

    def remove_h2(self):
        self.remove_datasource('ExampleDS')
        self.remove_jdbc_driver('h2')
