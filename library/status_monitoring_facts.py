#!/usr/bin/python
# Copyright (c) 2017-2019 Forcepoint
import logging


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: status_monitoring_facts
short_description: retrieve engine node status
description:
  - return engine node status for given engine/node

version_added: '2.5'

options:
  engine:
    description:
      - Engine to retrieve the status
    required: true
    type: str
  nodeid:
    description:
      - Node_id to retrieve the status
    required: true
    type: int
  
extends_documentation_fragment:
  - management_center
  - management_center_facts

requirements:
  - smc-python >= 1.0.24
author:
  - Forcepoint
'''


EXAMPLES = '''
- name: retrieve node status for engine myfirewall
  status_monitoring_facts:
    engine: myfirewall
    nodeid: 0

'''


RETURN = '''
status_monitoring_facts: 
    description: retrieve node status for given engine/node
    returned: always
    type: dict
    sample:
   {
    "ansible_facts": {
        "initial_license_remaining_days": 0,
        "licensed": true,
        "proof_of_serial": null,
        "state": {
            "active_policy": "asimpleanypolicy",
            "configuration_status": "Installed",
            "connectivity_status": "OK",
            "dyn_up": "1883",
            "engine_node_status": "Online",
            "installed_policy": "asimpleanypolicy",
            "installed_policy_ref": "https://localhost:8082/7.1/elements/fw_policy/1000044",
            "last_upload_time": 1748419095812,
            "monitoring_state": "READY",
            "monitoring_status": "OK",
            "name": "myfw3 node 1",
            "platform": "x86-64",
            "version": "version 7.3.1"
        }
    },

'''

from ansible.module_utils.smc_util import ForcepointModuleBase, is_licensed

try:
    from smc.core.engine import Engine
    from smc.api.exceptions import ElementNotFound, SMCException
except ImportError:
    pass

logger = logging.getLogger("smc")

class StatusMonitoringFacts(ForcepointModuleBase):
    def __init__(self, unit_test=False):
        
        self.module_args = dict(
            engine=dict(type='str'),
            nodeid = dict(type='int', default=1)
        )

        self.extra_args = None
        self.engine = None
        self.nodeid = None

        self.results = dict(
            ansible_facts=dict(
                state={}
            )
        )
        if not unit_test:
            super(StatusMonitoringFacts, self).__init__(self.module_args, is_fact=True)

    def exec_module(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        
        # Verify the engine specified
        if self.engine:
            try:
                fw = Engine.get(self.engine)
            except ElementNotFound:
                self.fail(
                    msg='Specified engine was not found: {}. Called from: {}'
                    .format(self.engine, self.__class__.__name__))

        if self.nodeid > len(fw.nodes) -1:
            logger.error("Node {} not found in {}:".format(self.nodeid, fw.nodes))
            raise SMCException('Node specified was not found. This engine '
                               'has %s nodes (numbering starts at 0)' % (len(fw.nodes)))
        node = fw.nodes.get(self.nodeid)
        self.results['ansible_facts'] = {'state': dict(node.status()),
                                         'licensed': is_licensed(node.name),
                                         'proof_of_serial':node.appliance_info().proof_of_serial,
                                         'initial_license_remaining_days': node.appliance_info().initial_license_remaining_days}
        return self.results

def main():
    StatusMonitoringFacts()
    
if __name__ == '__main__':
    main()
