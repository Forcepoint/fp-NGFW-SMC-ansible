#!/usr/bin/python
# Copyright (c) 2017-2019 Forcepoint


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: l3fw_policy_facts
short_description: Facts about firewall policies
description:
  - Provides information on linked policies such as inspection and
    the base level template.

version_added: '2.5'
  
extends_documentation_fragment:
  - management_center
  - management_center_facts

requirements:
  - smc-python
author:
  - Forcepoint
'''


EXAMPLES = '''
- name: Show all policies
  l3fw_policy_facts:
    
- name: Show policy information for policies contained 'Layer 3'
    l3fw_policy_facts:
      filter: Layer 3
'''


RETURN = '''
policies:
    description: Return all policies
    returned: always
    type: list
    sample: [{
        "name": "Master Engine Policy", 
        "type": "fw_policy"
        },
        {
        "name": "Layer 3 Router Policy", 
        "type": "fw_policy"
    }]

policies:
    description: Return policies with 'Layer 3' as filter
    returned: always
    type: list
    sample: [{
        "comment": null, 
        "inspection_policy": "High-Security Inspection Policy",
        "file_filtering_policy": "Legacy Anti-Malware",
        "name": "Layer 3 Virtual Firewall Policy",
        "tags": ['footag'], 
        "template": "Firewall Inspection Template", 
        "type": "fw_policy"
    }]
'''

from ansible.module_utils.smc_util import ForcepointModuleBase


try:
    from smc.policy.layer3 import FirewallPolicy
except ImportError:
    pass


def policy_dict_from_obj(element):
    """
    Resolve the category to the supported types and return a dict
    with the values of defined attributes
    
    :param Element element
    """
    elem = {
        'name': element.name,
        'type': element.typeof,
        'tags': [],
        'template': element.template.name,
        'inspection_policy': element.inspection_policy.name,
        'file_filtering_policy': element.file_filtering_policy.name 
            if element.file_filtering_policy else None,
        'comment': getattr(element, 'comment', None)}
    
    for tag in element.categories:
        elem['tags'].append(tag.name)
    
    return elem


class FWPolicyFacts(ForcepointModuleBase):
    def __init__(self):
        
        self.element = 'fw_policy'
        self.limit = None
        self.filter = None
        self.exact_match = None
        self.case_sensitive = None
        
        self.results = dict(
            ansible_facts=dict(
                policies=[]
            )
        )
        super(FWPolicyFacts, self).__init__({}, is_fact=True)

    def exec_module(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        
        result = self.search_by_type(FirewallPolicy)
        # Search by specific element type
        if self.filter:    
            elements = [policy_dict_from_obj(element) for element in result]
        else:
            elements = [{'name': element.name, 'type': element.typeof} for element in result]
        
        self.results['ansible_facts'] = {'policies': elements}
        return self.results

def main():
    FWPolicyFacts()
    
if __name__ == '__main__':
    main()
