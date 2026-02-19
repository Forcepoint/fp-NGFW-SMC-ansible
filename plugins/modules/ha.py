#!/usr/bin/python
#
# Copyright (c) 2017-2019 Forcepoint
import traceback

from smc.api.exceptions import SMCException
from smc.elements.servers import ManagementServer

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ha
short_description: Facts about High Availability in SMC
description:
  - Module that controls aspects of the HA System, such as set active or
set standby, etc.


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
- name: Examples of high availability commands
  collections:
    - forcepoint.fp_ngfw_smc_ansible
  hosts: localhost
  gather_facts: no
  tasks:

  - name: Launch full replication
    ha:
      smc_logging:
       level: 10
       path: ansible-smc.log
      name: Management Server
      operation: full_replication

  - name: Exclude from replication
    ha:
      smc_logging:
       level: 10
       path: ansible-smc.log
      name: Management Server
      operation: exclude

  - name: Launch activation of the specified management server
    ha:
      smc_logging:
       level: 10
       path: ansible-smc.log
      name: Management Server
      operation: set_active

  - name: Launch deactivation of the specified management server
    ha:
      smc_logging:
       level: 10
       path: ansible-smc.log
      name: Management Server
      operation: set_standby
'''


RETURN = '''
'''

from ansible_collections.forcepoint.fp_ngfw_smc_ansible.plugins.module_utils.smc_util import ForcepointModuleBase

try:
    from smc.core.ha_management import HAManagement  # noqa
except ImportError:
    pass


class HA(ForcepointModuleBase):
    def __init__(self, unit_test=False):
        
        self.module_args = dict(
            name=dict(type='str', required=True),
            operation=dict(type='str', choices=['full_replication', 'exclude', 'set_active', 'set_standby'], required=True)
        )
    
        self.name = None
        self.operation=None
        
        self.results = dict(
            ansible_facts=dict(
                infos=[]
            )
        )
        if not unit_test:
            super(HA, self).__init__(self.module_args, is_fact=False)


    def exec_module(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        try:
            server = ManagementServer(self.name)

            ha = HAManagement()
            results = ""
            if self.operation == "full_replication":
                results = ha.full_replication(server)
            elif self.operation == "exclude":
                results = ha.exclude(server)
            elif self.operation == "set_active":
                results = ha.set_active(server)
            elif self.operation == "set_standby":
                results = ha.set_standby(server)

        except SMCException as err:
            self.fail(msg=str(err), exception=traceback.format_exc())

        self.results['ansible_facts']["results"] = { "status": results }
        return self.results

def main():
    HA()
    
if __name__ == '__main__':
    main()
