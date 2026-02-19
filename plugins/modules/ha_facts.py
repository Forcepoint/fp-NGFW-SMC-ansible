#!/usr/bin/python
#
# Copyright (c) 2017-2019 Forcepoint


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: ha_facts
short_description: Facts about High Availability in SMC
description:
  - Module that controls aspects of the HA System, such as getting info or diagnostics.


version_added: '2.5'

options:
  
extends_documentation_fragment:
  - management_center
  - management_center_facts

requirements:
  - smc-python >= 1.27
author:
  - Forcepoint
'''
        

EXAMPLES = '''
- name: Examples of retrieving HA facts
  collections:
    - forcepoint.fp_ngfw_smc_ansible
  hosts: localhost
  gather_facts: no
  tasks:

  - name: Get High Availability details
    ha_facts:
      smc_logging:
       level: 10
       path: ansible-smc.log
'''


RETURN = '''
ha_facts: 
    description: When filtering by element, only top level meta is returned
    returned: always
    type: list
    sample:

{
  "ansible_facts": {
    "ha_infos": {
      "active_server": "Management Server",
      "connected_server": "Management Server"
    },
    "diagnostics": {
      "servers": [
        {
          "title": "Management Server",
          "messages": [
            {
              "msg": "    Primary IP address:127.0.0.1 / IP address in configuration: 127.0.0.1 / IP address detected by Java runtime: 127.0.1.1"
            },
            {
              "msg": "    Secondary IP addresses: "
            },
            {
              "msg": "    Contact IP addresses: Default:127.0.0.1 HQ:127.0.0.1 "
            },
            {
              "msg": "    License: 2028-01-01"
            },
            {
              "msg": "    Active Management Server: Management Server (10)"
            },
            {
              "msg": "    Login status: OK  - internal server key 10 - Management IP addresses: 127.0.0.1"
            }
          ]
        },
        {
          "title": "Log Server",
          "messages": [
            {
              "msg": "    Primary IP address:127.0.0.1 / IP address in configuration: ? / IP address detected by Java runtime: ?"
            },
            {
              "msg": "    Secondary IP addresses: "
            },
            {
              "msg": "    Contact IP addresses: Default:127.0.0.1 HQ:127.0.0.1 "
            },
            {
              "msg": "    License: 2028-01-01"
            },
            {
              "msg": "    Login status: KO  - Management IP addresses: N/A"
            }
          ]
        },
        {
          "title": "Web Portal Server",
          "messages": [
            {
              "msg": "    Primary IP address:127.0.0.1 / IP address in configuration: ? / IP address detected by Java runtime: ?"
            },
            {
              "msg": "    Secondary IP addresses: "
            },
            {
              "msg": "    Contact IP addresses: "
            },
            {
              "msg": "    License: No expiration date              "msg": "    License: No expiration date"
            },
            {
              "msg": "    Login status: KO  - Management IP addresses: N/A"
            }
          ]
        }
      ],
      "error": true
    }
  }
'''
from ansible_collections.forcepoint.fp_ngfw_smc_ansible.plugins.module_utils.smc_util import ForcepointModuleBase

try:
    from smc.core.ha_management import HAManagement  # noqa
except ImportError:
    pass

DIAGNOSTIC_ERRORS = ["(Isolated)", "Login status: KO"]
DIAGNOSTIC_TITLE_OK = "No issues were detected while running the diagnostic."


def check_diag_issue(check_for=None):
    to_return = {}
    diag = HAManagement().diagnostic()
    error_to_return = False
    info_to_return=[]
    for infob in diag.message:
        info={}
        info["server"] = infob.title
        msg_to_return = []
        for msg in infob.message:
            msg_to_return.append({"msg": msg})
            if check_for is not None:
                for message in check_for:
                    if message in msg:
                        error_to_return = True
        info["messages"] = msg_to_return
        info_to_return.append(info)
    to_return["servers"]=info_to_return

    # check for error messages
    infob = diag.errors_warnings
    if DIAGNOSTIC_TITLE_OK not in infob.title:
        error_to_return = True
    for msg in infob.message:
        if check_for is not None:
            for message in check_for:
                if message in msg:
                    error_to_return = True

    to_return["error"] = error_to_return
    return to_return


class HAFacts(ForcepointModuleBase):
    def __init__(self, unit_test=False):

        # No arguments
        self.module_args = dict()

        # Default arguments for facts
        self.limit = None
        self.filter = None
        self.exact_match = None
        self.case_sensitive = None
        
        self.results = dict(
            ansible_facts=dict(
                ha_infos={},
                diagnostics={}
            )
        )
        if not unit_test:
            super(HAFacts, self).__init__(self.module_args, is_fact=True)


    def exec_module(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        
        ha = HAManagement()
        # get HA infos
        infos = ha.get_ha()

        info_data = {"active_server":infos.active_server.name,
                     "connected_server":infos.connected_server.name}

        standby_data = [server.name for server in infos.standby_servers]
        if standby_data :
            info_data['standby_servers']=standby_data

        issues=check_diag_issue(DIAGNOSTIC_ERRORS)

        self.results['ansible_facts']["ha_infos"] = info_data
        self.results['ansible_facts']["diagnostics"] = issues
        return self.results

def main():
    HAFacts()
    
if __name__ == '__main__':
    main()
