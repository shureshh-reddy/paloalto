import yaml
import sys
import json
import os
import pprint
import difflib

from jycm.helper import make_ignore_order_func
from jycm.jycm import YouchamaJsonDiffer
from IPython import display
from scrapli.driver.core import IOSXEDriver, EOSDriver

# Global Constants

LINE = ('-' * 10)
MAX_PING_WAIT = 300
WAIT_BETWEEN_PING = 15
WAIT_AFTER_REBOOT = 60
WAIT_FOR_CONTROL_PLAIN_CONVERGENCE = 120

class AristaState:
    
    def __init__(self, commands=None):
        self.debug_commands = {'version_summary': {'command': 'show version | ', 'output': {}},
                                'route_summary': {'command': 'show ip route summary', 'output': {}},
                                'interface_status': {'command': 'show interfaces status connected', 'output': {}}
                            }
        if commands is not None:
            for command in commands:
                out = {'command': None, 'output': {}}
                out['command'] = command
                self.debug_commands[command] = out

        print(self.debug_commands)
    
    def find_key(self, data, target_key):
        for key, value in data.items():
            if isinstance(value, dict):
                yield from self.find_key(value, target_key)
            elif key == target_key:
                yield value
    
    def _set_running_version(self):
        output = self.find_key(self.debug_commands['version_summary']['output'], 'version')
        for item in output:
            self.running_version = item
    
    def _set_model_name(self):
        output = self.find_key(self.debug_commands['version_summary']['output'], 'modelName')
        for item in output:
            self.model_name = item

    def _set_total_routes(self):
        total_ip_routes = 0
        output = self.find_key(self.debug_commands['route_summary']['output'], 'totalRoutes')
        for item in output:
            total_ip_routes = int(item)
        self.total_ip_routes = total_ip_routes

    def populate(self, run_command):
        for k in self.debug_commands.keys():
            self.debug_commands[k]['output'] = \
                run_command(self.debug_commands[k]['command'])
        
        return self.debug_commands

class CiscoState:
    
    def __init__(self, commands=None):
        self.debug_commands = {'version_summary': {'command': 'show version | include uptime', 'output': {}},
                                'interface_status': {'command': 'show ip interface brief | exclude unassigned', 'output': {}}
                            }

        if commands is not None:
            for command in commands:
                out = {'command': None, 'output': {}}
                out['command'] = command
                self.debug_commands[command] = out
    
    def find_key(self, data, target_key):
        for key, value in data.items():
            if isinstance(value, dict):
                yield from self.find_key(value, target_key)
            elif key == target_key:
                yield value
    
    def _set_running_version(self):
        output = self.find_key(self.debug_commands['version_summary']['output'], 'version')
        for item in output:
            self.running_version = item
    
    def _set_model_name(self):
        output = self.find_key(self.debug_commands['version_summary']['output'], 'modelName')
        for item in output:
            self.model_name = item

    def _set_total_routes(self):
        total_ip_routes = 0
        output = self.find_key(self.debug_commands['route_summary']['output'], 'totalRoutes')
        for item in output:
            total_ip_routes = int(item)
        self.total_ip_routes = total_ip_routes

    def populate(self, run_command):
        for k in self.debug_commands.keys():
            self.debug_commands[k]['output'] = \
                run_command(self.debug_commands[k]['command'])
        
        return self.debug_commands

class DeviceHandler:

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.device = {
            "host": self.ip_address,
            "auth_username": "cisco",
            "auth_password": "cisco",
            "auth_strict_key": False,
            "ssh_config_file": '~/.ssh/config'
        }
    
    def arista_run_command(self, cmd):
        try:
            with EOSDriver(**self.device) as conn:
                resp = conn.send_command(cmd)
                #output = resp.textfsm_parse_output()
                #return output
                return resp
        except Exception as e:
            print(e)
            return None
    
    def cisco_run_command(self, cmd):
        try:
            with IOSXEDriver(**self.device) as conn:
                resp = conn.send_command(cmd)
                #output = resp.textfsm_parse_output()
                #return output
                return resp
        except Exception as e:
            print(e)
            return None


def main():
    #try:
    #    operation_method = sys.argv[1]
    #    rpd_id = sys.argv[2]
    #    date = sys.argv[3]
    #    file_name = sys.argv[4]
    #except Exception as e:
    #    pass
    '''
    try:
        operation_method = input('Enter operation method "pre" or "post": ')
        rpd_id = input('Enter RPD id: ')  #need to remove rpd characters
        date = input('Enter date in MM-DD-YY format: ')
        file_name = input('Device details file path: ')
    except Exception as e:
        pass
    '''

    try:
        operation_method = input('Enter operation method "pre" or "post": ')
        rpd_id = '722544'
        date = '09-03-21'
        file_name = 'change_device.yml'
    except Exception as e:
        pass

    

    if operation_method.lower() == 'pre' or operation_method.lower() == 'post':
        with open(file_name, 'r') as f:
            user_data = yaml.load(f)
        state = []
        os_types = user_data['devices'].keys()
        for device_os in os_types:
            for each_os in user_data['devices'][device_os]:
                ip_address = each_os['ip_address']
                commands = each_os['commands']

                for ip in ip_address:
                    device_state = DeviceHandler(ip)
                    if device_os.lower() == 'arista_eos':
                        if commands is not None:
                            arista_config = AristaState(commands)
                            state_output = arista_config.populate(device_state.arista_run_command)
                            state.append(state_output)

                    elif device_os.lower() == 'cisco_ios':
                        if commands is not None:
                            cisco_config = CiscoState(commands)
                            state_output = cisco_config.populate(device_state.cisco_run_command)
                            state.append(state_output)
							
                    with open(rpd_id+'_'+date+'_'+'.json', 'w') as file:
                        json.dump(device_state, file, indent=4)

        
        #if os.path.exists('pre_'+rpd_id+'.json') and os.path.exists('post_'+rpd_id+'.json'):
        #    with open('pre_'+rpd_id+'.json', 'r') as prefile:
        #        pre_data = json.load(prefile)
        #    with open('post_'+rpd_id+'.json', 'r') as postfile:
        #        post_data = json.load(postfile)

            '''
            difference = difflib.HtmlDiff(tabsize=2)

            with open("compare.html", "w") as fp:
                html = difference.make_file(fromlines=pre_data, tolines=post_data, fromdesc="Original", todesc="Modified")
                fp.write(html)

			'''
    
    

if __name__ == "__main__":
    main()
