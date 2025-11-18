#!/usr/bin/python
# Copyright (c) 2017-2019 Forcepoint
import logging
from collections import defaultdict


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: status_monitoring_facts
short_description: Retrieve engine node status and health information
description:
  - Returns detailed status information for engine nodes
  - Provides health, hardware, and interface status for comprehensive monitoring
  - Organizes hardware status by type and sorts interfaces by ID

version_added: '2.5'

options:
  engine:
    description:
      - Engine name to retrieve the status
    required: true
    type: str
  nodeid:
    description:
      - Node_id to retrieve the status
    required: false
    type: int
    default: 1
  wait_for_online:
    description:
      - Wait for node to be online before retrieving status
    required: false
    default: false
    type: bool
  max_wait:
    description:
      - Maximum time to wait (in minutes) for node to come online when wait_for_online is true
    required: false
    default: 3
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

- name: Get status for all nodes with hardware and interface information
  status_monitoring_facts:
    engine: myfirewall

- name: Get status with online check
  status_monitoring_facts:
    engine: myfirewall
    wait_for_online: true
    max_wait: 5
'''


RETURN = '''
status_monitoring_facts: 
    description: retrieve node status for given engine/node
    returned: always
    type: dict
    sample:
   {
    "ansible_facts": {
        "engine_name": "Helsinki",
        "Helsinki node 1": {
            "node_id": 1,
            "status": "Online",
            "hardware_status": {...},
            "interface_status": {...},
            "status_info": {...}
        },
        "Helsinki node 2": {
            "node_id": 2,
            "status": "Online",
            "hardware_status": {...},
            "interface_status": {...},
            "status_info": {...}
        }
    }
   }
'''

from ansible_collections.forcepoint.fp_ngfw_smc_ansible.plugins.module_utils.smc_util import ForcepointModuleBase, is_licensed

try:
    from smc.core.engine import Engine
    from smc.core.waiters import NodeStatusWaiter
    from smc.api.exceptions import ElementNotFound, SMCException
except ImportError:
    pass

logger = logging.getLogger("smc")

class StatusMonitoringFacts(ForcepointModuleBase):
    def __init__(self, unit_test=False):
        
        self.module_args = dict(
            engine=dict(type='str', required=True),
            nodeid=dict(type='int', default=None),
            wait_for_online=dict(type='bool', default=False),
            max_wait=dict(type='int', default=3)
        )

        self.engine = None
        self.nodeid = None
        self.wait_for_online = None
        self.max_wait = None

        # Initialize with engine_name and empty nodes list for backward compatibility
        self.results = dict(
            ansible_facts=dict(
                engine_name="",
                nodes={}
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
                # Add engine name to results
                self.results['ansible_facts']['engine_name'] = self.engine
            except ElementNotFound:
                self.fail(
                    msg='Specified engine was not found: {}. Called from: {}'
                    .format(self.engine, self.__class__.__name__))

        # If specific nodeid is provided, get status for just that node
        if self.nodeid is not None:
            if self.nodeid > len(fw.nodes) - 1:
                logger.error("Node {} not found in {}:".format(self.nodeid, fw.nodes))
                raise SMCException('Node specified was not found. This engine '
                                   'has %s nodes (numbering starts at 0)' % (len(fw.nodes)))
            node = fw.nodes.get(self.nodeid)

            # Get status and other info
            status_info = dict(node.status())
            node_name = status_info.get('name', f"node_{self.nodeid}")

            node_info = {
                'node_id': self.nodeid,
                'status': status_info.get('engine_node_status', 'Unknown'),
                'status_info': status_info,
                'licensed': is_licensed(node.name),
                'proof_of_serial': node.appliance_info().proof_of_serial,
                'initial_license_remaining_days': node.appliance_info().initial_license_remaining_days
            }

            # For backwards compatibility
            self.results['ansible_facts']['state'] = status_info
            self.results['ansible_facts']['licensed'] = node_info['licensed']
            self.results['ansible_facts']['proof_of_serial'] = node_info['proof_of_serial']
            self.results['ansible_facts']['initial_license_remaining_days'] = node_info['initial_license_remaining_days']
            self.results['ansible_facts']['nodes'] = [{'name': node_name, **node_info}]

            # Add node info with node name as the key
            self.results['ansible_facts'][node_name] = node_info

            return self.results

        # Otherwise get detailed status for all nodes
        nodes_list = []  # For backward compatibility

        for node in fw.nodes:
            node_info = {}

            # Basic node info
            node_id = node.nodeid

            # Wait for node to be Online if requested
            if self.wait_for_online:
                waiter = NodeStatusWaiter(node, 'Online', max_wait=self.max_wait)
                while not waiter.done():
                    status = waiter.result(5)  # Check every 5 seconds
                node_status = status if status else 'Offline'
                status_info = node.status() if node_status == 'Online' else {}
            else:
                # Just get current status
                status_info = node.status()
                if status_info and 'engine_node_status' in status_info:
                    node_status = status_info['engine_node_status']
                else:
                    node_status = 'Unknown'

            node_name = status_info.get('name', f"node_{node_id}")

            # Add basic info
            node_info['node_id'] = node_id
            node_info['status'] = node_status
            node_info['status_info'] = status_info
            node_info['licensed'] = is_licensed(node.name)
            try:
                appliance_info = node.appliance_info()
                node_info['proof_of_serial'] = appliance_info.proof_of_serial
                node_info['initial_license_remaining_days'] = appliance_info.initial_license_remaining_days
            except Exception:
                node_info['proof_of_serial'] = None
                node_info['initial_license_remaining_days'] = 0

            # Hardware status - simplified flat structure
            try:
                hardware_status = {}
                for hw_item in node.hardware_status:
                    if hasattr(hw_item, 'name') and hasattr(hw_item, 'status'):
                        # For Label type objects with items
                        if hasattr(hw_item, 'items') and hw_item.items:
                            subsystem_name = hw_item.name
                            subsystem_status = hw_item.status

                            # Create a section for this subsystem
                            hardware_status[subsystem_name] = {
                                'status': subsystem_status,
                                'components': {}
                            }

                            # Add each component as a direct entry with key values
                            for item in hw_item.items:
                                component_name = item.get('name', '')
                                component_info = {
                                    'status': item.get('status', ''),
                                    'value': item.get('value', '')
                                }

                                # If there are detailed statuses, add them as key-value pairs
                                if 'statuses' in item and item['statuses']:
                                    for detail in item['statuses']:
                                        param = detail.get('param', '')
                                        value = detail.get('value', '')
                                        if param and value:
                                            component_info[param] = value

                                hardware_status[subsystem_name]['components'][component_name] = component_info
                        else:
                            # Simple hardware items
                            hw_dict = vars(hw_item)
                            hw_name = hw_dict.get('name', 'unknown')
                            hw_info = {}

                            for key, value in hw_dict.items():
                                if not key.startswith('_') and key != 'name':
                                    # Ensure value is JSON serializable
                                    if hasattr(value, '__dict__'):
                                        hw_info[key] = vars(value)
                                    else:
                                        hw_info[key] = value

                            hardware_status[hw_name] = hw_info

                node_info['hardware_status'] = hardware_status
            except Exception as e:
                node_info['hardware_status'] = {'error': str(e)}

            # Interface status - organize as a dictionary keyed by interface name
            try:
                interfaces = {}
                for iface in node.interface_status:
                    if_dict = {}
                    for attr in ['interface_id', 'name', 'status', 'speed_duplex',
                                'mtu', 'capability', 'flow_control', 'port',
                                'aggregate_is_active', 'aggregate_mode',
                                'aggregate_slaves', 'aggregate_master',
                                'aggregate_master_status']:
                        if hasattr(iface, attr):
                            if_dict[attr] = getattr(iface, attr)

                    # Use interface name as the key if available, otherwise use ID
                    interface_name = if_dict.get('name')
                    if interface_name:
                        interfaces[interface_name] = if_dict
                    else:
                        # Fall back to ID if name is not available
                        interface_id = if_dict.get('interface_id')
                        if interface_id is not None:
                            interfaces[f"interface_{interface_id}"] = if_dict
                        else:
                            # For interfaces without name or ID, append to a special list
                            if 'unknown' not in interfaces:
                                interfaces['unknown'] = []
                            interfaces['unknown'].append(if_dict)

                node_info['interface_status'] = interfaces
            except Exception as e:
                node_info['interface_status'] = {'error': str(e)}

            # For backward compatibility - add to nodes list
            nodes_list.append({'name': node_name, **node_info})

            self.results['ansible_facts']['nodes'][node_name] = node_info

        return self.results

def main():
    StatusMonitoringFacts()
    
if __name__ == '__main__':
    main()
