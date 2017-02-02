from lib import actions, ztp_utils, Secure_Copy
import os, sys
import time

class Login_SaveAction(actions.SessionAction):
    def __init__(self,config):
        super(Login_SaveAction, self).__init__(config)
        self._username = self.config['ztp_username']
        self._password = self.config['ztp_password']
        self._temp_dir = self.config['temp_dir']
        self._prod_username = self.config['prod_username']
        self._prod_password = self.config['prod_password']

    def run(self,prod_ip, username='', password='', prod_username='',prod_password=''):
        # delay since last task reloaded switch
        self._filename = "%s%s" % (self._temp_dir, prod_ip)
        ztp_utils.replace_default_userpass(self, username, password, prod_username, prod_password)
        print "Username: "+self._username+"  Password: "+self._password
        print "prod_user: "+self._prod_username+"   prod_pw: "+self._prod_password
        session=ztp_utils.start_session(prod_ip, prod_username, prod_password, prod_username, prod_password, 'ssh')
        if session.login():
            if session.enter_enable_mode():
               command='wr mem'
               (success, results) = ztp_utils.send_commands_to_session(session, command, conf_mode=True)
               if success:
                   scp=Secure_Copy.Secure_Copy(prod_ip, self._prod_username, self._prod_password)
                   if scp.get_file('StartConfig', self._filename):
                       session.logout()
                       return (True, "Success")
                   else:
                       session.logout()
                       return (False, "Unable to scp startup config.")
        else:
            session.logout()
            return (False, "Unable to send login.")
