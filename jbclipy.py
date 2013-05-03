import os,platform

class JBCliPy():

    """Constructor"""    
    def __init__(self,username=None,password=None,win_suppress=False):

        if username and password:
            self.connect = ' --user='  + username + ' --password=' + password
        else:
            self.connect = ''
            
        if platform.system() == 'Windows':
            self.connect = 'jboss-cli.bat -c' + self.connect + ' --commands=batch,<>,run-batch'
            if win_suppress:
                self.connect = ' < nul'
        else:
            self.connect = 'jboss-cli.sh -c' + self.connect + ' --commands=batch,<>,run-batch'
            
        self.commands = []
    

    """User Actions"""
    def execute(self):
        savedPath = os.getcwd()
        os.chdir(os.environ["JBOSS_HOME"]+"/bin")
        os.system(self.connect.replace('<>',','.join(self.commands)))
        os.chdir(savedPath)
        self.reset()

    def reset(self):
        self.commands = []

    def print_execution(self):
        print self.connect.replace('<>',','.join(self.commands))
        
    def print_commands(self):
        print ','.join(self.commands)

    """Build Methods"""
    def custom(self,cmd):
        self.commands.append(cmd)
        
    def remove_subsystem(self,subsystem):
        self.commands.append('/subsystem=%s:remove()' % subsystem)

    def add_extension(self,extension):
        self.commands.append('/extension=%s:add()' % extension)
        
    def remove_extension(self,extension):
        self.commands.append('/extension=%s:remove()' % extension)

    def remove_socket_binding(self,binding):
        self.commands.append('/socket-binding-group=standard-sockets/socket-binding=%s:remove()' % binding)

    def add_connector(self,name,protocol,scheme,socket_binding):
        self.commands.append('/subsystem=web/connector=%s:add(name=%s,protocol=%s,scheme=%s,socket-binding=%s)' % (name,name,protocol,scheme,socket_binding))

    def remove_connector(self,name):
        self.commands.append('/subsystem=web/connector=%s:remove()' % name)

    def add_console_handler(self,name,
                           autoflush=None,
                           encoding=None,
                           filter=None,
                           formatter='%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n',
                           level='INFO',
                           target=None):
        
        s = '/subsystem=logging/console-handler=%s:add(name=%s' % (name,name)
        if autoflush:
            s = s + ',autoflash=' + autoflush
        if encoding:
            s = s + ',encoding=' + encoding
        if filter:
            s = s + ',filter=' + filter
        if formatter:
            s = s + ',formatter="%s"' % formatter
        if level:
            s = s + ',level=' + level
        if target:
            s = s + ',target=' + target

        self.commands.append(s + ')')


    def add_periodic_rotating_file_handler(self,name,
                                           file,
                                           append='true',
                                           autoflush=None,
                                           encoding=None,
                                           filter=None,
                                           formatter='%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n',
                                           level='INFO',
                                           suffix='.yyyy-MM-dd'):

        s = '/subsystem=logging/periodic_rotating_file_handler=%s:add(name=%s,file={"relative-to"=>"%s","path"=>"%s"}' % (name,name,file[0],file[1])
        if append:
            s = s + ',append=' + append
        if autoflash:
            s = s + ',autoflush=' + autoflush
        if encoding:
            s = s + ',encoding=' + encoding
        if filter:
            s = s + ',filter=' + filter
        if formatter:
            s = s + ',formatter=' + formatter
        if level:
            s = s + ',level=' + level
        if suffix:
            s = s + ',suffix=' + suffix

        self.commands.append(s + ')')
                                           

    def add_size_rotating_file_handler(self,name,
                                       file,
                                       rotate_size,
                                       append='true',
                                       autoflush=None,
                                       encoding=None,
                                       filter=None,
                                       formatter='%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n',
                                       level='INFO',
                                       max_backup_index=None):
                                       
        s = '/subsystem=logging/size_rotating_file_handler=%s:add(name=%s,file={"relative-to"=>"%s","path"=>"%s"},rotate-size=%s' % (name,name,file[0],file[1],rotate_size)
        if append:
            s = s + ',append=' + append
        if autoflash:
            s = s + ',autoflush=' + autoflush
        if encoding:
            s = s + ',encoding=' + encoding
        if filter:
            s = s + ',filter=' + filter
        if formatter:
            s = s + ',formatter=' + formatter
        if level:
            s = s + ',level=' + level
        if max_backup_index:
            s = s + ',max-backup-index=' + max_backup_index

        self.commands.append(s + ')')

    def add_logger(self,name,handlers,level='ALL'):
        s = '/subsystem=logging/logger=%s:add(level=%s,handlers=[' % (name,level)
        for handler in handlers:
            s = s + '"%s",' % handler
        s = s[:-1] + '])'
        self.commands.append(s)

    def add_handler_to_root_logger(self,name):
        self.commands.append('/subsystem=logging/root-logger=ROOT:root-logger-assign-handler(name="%s")' % name)


    def add_jdbc_driver(self,name,module,xa_class=None):
        s = '/subsystem=datasources/jdbc-driver=%s:add(driver-name=%s,driver-module-name=%s' % (name,name,module)

        if xa_class:
            s = s + ',driver-xa-datasource-class-name=%s)' % xa_class
        else:
            s = s + ')'

        self.commands.append(s)

    def remove_jdbc_driver(self,name):
        self.commands.append('/subsystem=datasources/jdbc-driver=%s:remove()' % name)

    def add_datasource(self,name,jndi,url,driver,username,password):
        self.commands.append('/subsystem=datasources/data-source=%s:add(jndi-name="%s",connection-url="%s",driver-name="%s",user-name="%s",password="%s",use-java-context=true)' % (name,jndi,url,driver,username,password))

    def remove_datasource(self,name):
        self.commands.append('/subsystem=datasources/data-source=%s:remove()' % name)

    def enable_datasource(self,name):
        self.commands.append('/subsystem=datasources/data-source=%s:enable()' % name)

    def disable_datasource(self,name):
        self.commands.append('/subsystem=datasources/data-source=%s:disable()' % name)

    def test_datasource(self,name):
        self.commands.append('/subsystem=datasources/data-source=%s:test-connection-in-pool' % name)

    def add_xa_datasource(self,name,jndi,url,driver,username,password):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:add(jndi-name="%s",connection-url="%s",driver-name="%s",user-name="%s",password="%s",use-java-context=true)' % (name,jndi,url,driver,username,password))

    def remove_xa_datasource(self,name):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:remove()' % name)
        
    def enable_xa_datasource(self,name):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:enable()' % name)

    def disable_xa_datasource(self,name):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:disable()' % name)

    def test_xa_datasource(self,name):
        self.commands.append('/subsystem=datasources/xa-data-source=%s:test-connection-in-pool' % name)



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
        if https:
            scheme = 'https'
        else:
            scheme = 'http'
        self.add_connector('ajp','AJP/1.3',scheme,'ajp')

        
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
