"""
Copyright 2016 Brocade Communications Systems, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json, os, time
import re
from lib import actions
from lib import ztp_utils, Secure_Copy

class GetFlashAction(actions.SessionAction):
    def __init__(self, config):
        super(GetFlashAction, self).__init__(config)
        self._config_archive_dir=self.config['config_backup_dir']

    def run(self, via, device, username='', password='', enable_username='', enable_password=''):
        ztp_utils.replace_default_userpass(self, username, password,
                                           enable_username, enable_password)
        session = ztp_utils.start_session(device, self._username, self._password,
                                          self._enable_username, self._enable_password, 'ssh')

        command = 'wr mem'
        (success, results) = ztp_utils.send_commands_to_session(session, command, conf_mode=False)
        print results
        # grab the config
        config_dir='%s/%s' % (self._config_archive_dir, device)
        print config_dir
        try:
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
        except IOError:
            sys.sterr.write("Could not create directory: ' %s' \r\n" % device)
            return(False,"Failed")
        scp=Secure_Copy.Secure_Copy(device,self._username,self._password)
        timestamp=int(time.time())
        filename= '%s/%s_%s.cfg' % (config_dir,device,timestamp)
        if scp.get_file('RunConfig', filename):
            return(True,"Success")
        return(False,"Failed")

