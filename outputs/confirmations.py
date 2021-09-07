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
        self.debug_commands = {'version_summary': {'command': 'show version', 'output': {}},
                                'route_summary': {'command': 'show ip route summary', 'output': {}},
                                'interface_status': {'command': 'show interfaces status connected', 'output': {}}
                            }
        if commands is not None:
            for command in commands:
                out = {'command': None, 'output': {}}
                out['command'] = command
                self.debug_commands[command] = out

        print(self.debug_commands)

        #self.running_version = None
        #self.model_name = None
        #self.total_ip_routes = None
    
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
        #self._set_model_name()
        #self._set_running_version()
        #self._set_total_routes()
        #return

class CiscoState:
    
    def __init__(self, commands=None):
        self.debug_commands = {'version_summary': {'command': 'show version', 'output': {}},
                                'route_summary': {'command': 'show ip route summary', 'output': {}},
                                'interface_status': {'command': 'show interfaces status connected', 'output': {}}
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
            "auth_username": "admin",
            "auth_password": "admin123",
            "auth_strict_key": False
        }
    '''
    def connect_to_device(self):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            ssh_conn = ConnectHandler(**self.auth_details)
            print('{} SSH TEST: PASS {}'.format(LINE, LINE))
            ssh_conn.enable()
            os_details = ssh_conn.send_command('show version')
            if 'Arista' in os_details:
                return 'Arista'
            elif 'Cisco' in os_details:
                return 'Cisco'

        except NetmikoTimeoutException as ne:
            print('SSH TEST: FAIL, ERROR: {}'.format(ne))
        except AuthenticationException as ae:
            print('SSH TEST: FAIL, ERROR: {}'.format(ae))
        except SSHException as se:
            print('SSH TEST: FAIL, ERROR: {}'.format(se))
        except Exception as e:
            print('SSH TEST: FAIL, ERROR: {}'.format(e))
    '''
    
    def arista_run_command(self, cmd):
        try:
            with EOSDriver(**self.device) as conn:
                resp = conn.send_command(cmd)
                output = resp.textfsm_parse_output()
                return output
        except Exception as e:
            print(e)
            return None
    
    def cisco_run_command(self, cmd):
        try:
            with IOSXEDriver(**self.device) as conn:
                resp = conn.send_command(cmd)
                output = resp.textfsm_parse_output()
                return output
        except Exception as e:
            print(e)
            return None


def main():
    try:
        operation_method = sys.argv[1]
        rpd_id = sys.argv[2]
        file_name = sys.argv[3]
    except Exception as e:
        pass

    if operation_method.lower() == 'pre' or operation_method.lower() == 'post':
        with open(file_name, 'r') as f:
            user_data = yaml.load(f)
        
        ip_address = user_data['devices']['ip_address']
        os_type = user_data['devices']['os_type']
        commands = user_data['devices']['commands']

        for ip in ip_address:
            device_state = DeviceHandler(ip)
            if os_type.lower() == 'arista_eos':
                if commands is not None:
                    arista_config = AristaState(commands)
                    state_output = arista_config.populate(device_state.arista_run_command)
                    with open(operation_method+'_'+rpd_id+'.json', 'a') as file:
                        json.dump(state_output, file, indent=4)
            elif os_type.lower() == 'cisco_ios':
                if commands is not None:
                    cisco_config = CiscoState(commands)
                    state_output = cisco_config.populate(device_state.cisco_run_command)
                    with open(operation_method+'_'+rpd_id+'.json', 'a') as file:
                        json.dump(state_output, file, indent=4)
        
        if os.path.exists('pre_'+rpd_id+'.json') and os.path.exists('post_'+rpd_id+'.json'):
            with open('pre_'+rpd_id+'.json', 'r') as prefile:
                pre_data = json.load(prefile)
            with open('post_'+rpd_id+'.json', 'r') as postfile:
                post_data = json.load(postfile)

            #difference = difflib.HtmlDiff(tabsize=2)

            #with open("compare.html", "w") as fp:
            #    html = difference.make_file(fromlines=pre_data, tolines=post_data, fromdesc="Original", todesc="Modified")
            #    fp.write(html)

            #display.HTML(open("compare.html", "r").read())

            ycm = YouchamaJsonDiffer(pre_data, post_data, ignore_order_func=make_ignore_order_func([
                "^set_in_set$",
                "^set_in_set->\\[\\d+\\]->set$"
            ]))

            ycm.diff()

            expected = {
                'list:add': [
                    {'left': '__NON_EXIST__', 'right': 2, 'left_path': '', 'right_path': 'set_in_set->[1]->set->[1]'}
                ],
                'list:remove': [
                    {'left': 5, 'right': '__NON_EXIST__', 'left_path': 'set_in_set->[0]->set->[1]', 'right_path': ''}
                ],
                'value_changes': [
                    {'left': 'label:1', 'right': 'label:1111', 'left_path': 'set_in_set->[0]->label',
                    'right_path': 'set_in_set->[1]->label', 'old': 'label:1', 'new': 'label:1111'}
                ]
            }

            assert ycm.to_dict(no_pairs=True) == expected
    
    

if __name__ == "__main__":
    main()
