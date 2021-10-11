import yaml
import json
import re
import os
from scrapli.driver.core import IOSXEDriver, EOSDriver

class DeviceState:

    def __init__(self, host_command = None, commands=None, static_commands=None, conn=None, string=None):
        self.debug_commands = static_commands
        self.host_command = host_command
        self.conn = conn
        self.encrypt_strings = string
        self.debug_output = {}
        if commands is not None:
            for command in commands:
                out = {'command': None, 'output': {}}
                out['command'] = command
                self.debug_commands[command] = out

    def populate(self):
        resp = self.conn.send_command(self.host_command)
        output = resp.textfsm_parse_output()
        hostname = output[0]['hostname']

        for k in self.debug_commands.keys():
            self.debug_output[hostname+'_'+k] = {}
            cmd = self.debug_commands[k]['command']
            self.debug_output[hostname+'_'+k]['command'] = cmd
            self.debug_output[hostname+'_'+k]['output'] = self.run_command(self.debug_commands[k]['command'])

        return hostname, self.debug_output

    def run_command(self, cmd):
        try:
            resp = self.conn.send_command(cmd)
            data = resp.result
            output = data.split("\n")
            output_data = []
            for data in output:
                count = 0
                for item in self.encrypt_strings:
                    if item in data:
                        n = re.sub('(?<={})(.*)'.format(item), ' ***********', count=2000, string=data)
                        output_data.append(n)
                        break
                    else:
                        count+=1
                    if len(self.encrypt_strings) == count:
                        output_data.append(data)
            return output_data

        except Exception as e:
            print(e)
            return None

def main():
    try:
        operation_method = input('Enter operation method "pre" or "post": ')
        rpd = input('Enter RPD id: ')
        date = input('Enter date in MM-DD-YY format: ')
        file_name = input('Device details file path: ')
    except Exception as e:
        pass

    pwd = os.getcwd()
    rpd_id = re.sub("\D", "", rpd)
    
    cisco_commands = {'version_summary': {'command': 'show version | include uptime', 'output': {}},
                      'running_config': {'command': 'show running-config', 'output': {}}
                    }

    arista_commands = {'version_summary': {'command': 'show version | include Uptime', 'output': {}},
                      'running_config': {'command': 'show running-config', 'output': {}}
                    }
    arista_encrypt_strings = ['enable secret',
                 'chap password',
                 'pap password',
                 'password', 
                 'secret', 
                 '.*wpa-psk ascii', 
                 '.*key',
                 'tacacs-server', 
                 'crypto isakmp key', 
                 'snmp-server community', 
                 'ospf message-digest-key',
                 'ospf authentication-key',
                 'authentication text',
                 'authentication md5 key-string'
                 'authentication',
                 'radius server',
                 'tacacs sever',
                 'key-string'
                 ]
    

    if operation_method.lower() == 'pre' or operation_method.lower() == 'post':
        with open(file_name, 'r') as f:
            user_data = yaml.load(f)
        os_types = user_data['devices'].keys()

        rpd_dir_path = os.path.join(pwd, rpd_id)
        if not os.path.exists(rpd_dir_path):
            os.mkdir(rpd_dir_path)
        
        if operation_method.lower() == 'pre':
            config_file_path = os.path.join(rpd_dir_path, date+'.txt')
            f = open(config_file_path, 'w')
            f.close()
            
        elif operation_method.lower() == 'post':
            rpd_file_path = os.path.join(pwd, rpd_id)
            dir_list = os.listdir(rpd_file_path)
            config_file_path = os.path.join(rpd_dir_path, dir_list[0])
            f = open(config_file_path, 'w')
            f.close()
        
        for device_os in os_types:
            for each_os in user_data['devices'][device_os]:
                ip_address = each_os['ip_address']
                commands = each_os.get('commands')

                for ip in ip_address:
                    config_state = []
                    device = {
                    "host": ip,
                    "auth_username": "cisco",
                    "auth_password": "cisco",
                    "auth_secondary": "cisco",
                    "auth_strict_key": False,
                    "transport": "system",
                    "ssh_config_file": '~/.ssh/config'
                    }
                    if device_os.lower() == 'arista_eos':
                        out = {}
                        try:
                            with EOSDriver(**device) as conn:
                                arista_config = DeviceState('show hostname', commands, arista_commands, conn, string=arista_encrypt_strings)
                                hostname, state_output = arista_config.populate()
                                out[hostname] = state_output
                                config_state.append(out)
                        except Exception as e:
                            print(e)

                    elif device_os.lower() == 'cisco_ios':
                        device["transport"] = "telnet"
                        out = {}
                        try:
                            with IOSXEDriver(**device) as conn:
                                cisco_config = DeviceState('show version', commands, cisco_commands, conn)
                                hostname, state_output = cisco_config.populate()
                                out[hostname] = state_output
                                config_state.append(out)
                        except Exception as e:
                            print(e)

                    with open(config_file_path, 'a') as file:
                        json.dump(config_state, file, indent=4)

if __name__ == "__main__":
    main()
