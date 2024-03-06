#!/usr/bin/python
# Copyright (c) 2017-2019 Forcepoint
ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: generic_element
short_description: Create, modify or delete elements inheriting from Element
description:
  - This module allows elements that inherit from smc.base.model.Element to be
    created, deleted or modified. Any valid smc-python element is one that has a
    direct entry point in the SMC API. In order to create an element, you must
    provide any attributes required by the elements create signature.
    This module uses an 'update or create' logic, therefore it is not possible to create
    the same element twice. If the element exists and the attributes provided are 
    different, the element will be updated before returned.

version_added: '2.5'

options:
  elements:
    description:
      - A list of the elements to create, modify or remove
    type: list
    required: true
    suboptions:
      element:
        description:
          - Specify the typeof attribute for the given element. This value is the API
            entry point that correlates to the given smc-python object instance
        type: dict
        suboptions:
          name:
            description:
              - Name of this host element
            type: str
            required: true
          kwargs:
            description:
              - Free flowing keyword arguments used to modify or create the element.
                Arg type values must conform to the create or update_or_create
                constructor for the element type
            type: complex
            required: false

extends_documentation_fragment:
  - management_center
 
requirements:
  - smc-python
author:
  - Forcepoint
'''

EXAMPLES = '''
- name: Create a VPN Profile
  generic_element:
    smc_logging:
      level: 10
      path: ansible-smc.log
    elements:
    - vpn_profile: 
        name: MyVPNProfile
        comment: mycomment
        capabilities:
          aes256_for_ike: True
          aes256_for_ipsec: True
          dh_group_2_for_ike: True
          esp_for_ipsec: True
          ike_v2: True
          main_mode: True
          pre_shared_key_for_ike: True
          sa_per_net: True
          sha1_for_ike: True
          sha1_for_ipsec: True
          sha2_ike_hash_length: 256
          sha2_ipsec_hash_length: 256
          vpn_client_rsa_signature_for_ike: True
          vpn_client_sa_per_net: True
'''

RETURN = '''
changed:
  description: Whether or not an element was changed
  returned: always
  type: bool
state:
  description: Full json definition of NGFW
  returned: always
  type: list
  sample: [
    {
        "action": "none", 
        "name": "MyVPNProfile", 
        "typeof": "vpn_profile"
    }
]
'''

import traceback
from ansible.module_utils.smc_util import ForcepointModuleBase
import logging

try:
    from smc.api.exceptions import SMCException
    from smc.base.collection import Search
    from smc.base.model import lookup_class, Element
    from smc.api.common import fetch_meta_by_name
except ImportError:
    pass

logger = logging.getLogger("smc")


class GenericElement(ForcepointModuleBase):
    def __init__(self):

        self.module_args = dict(
            elements=dict(type='list', required=True),
            state=dict(default='present', type='str', choices=['present', 'absent'])
        )
        self.elements = None

        self.results = dict(
            changed=False,
            state=[]
        )

        self.check_mode = False

        super(GenericElement, self).__init__(self.module_args, supports_check_mode=True)

    def exec_module(self, **kwargs):
        logger.debug("data={}".format(kwargs))
        state = kwargs.pop('state', 'present')
        for name, value in kwargs.items():
            setattr(self, name, value)

        # Validate whether the element type is valid
        entry_points = Search.object_types()

        for element in self.elements:
            for typeof, element_data in element.items():
                if typeof not in entry_points:
                    self.fail(msg='The specified element type: %s is not valid. '
                        'Data provided: %s' % (typeof, element))
                if 'name' not in element_data:
                    self.fail(msg='The name field is required to operate on all '
                        'elements. Data provided: %s' % element)

        try:
            if self.check_mode:
                return self.results

            for element in self.elements:
                logger.debug("Element={} type={}".format(element, type(element)))
                for typeof, data in element.copy().items():
                    try:
                        logger.debug("Update_or_create: Typof={} Data={}".format(typeof, data))
                        json_payload = dict()
                        for attribute, value in data.copy().items():
                            logger.debug("attribute={} value={}".format(attribute, value))
                            if type(value) is dict:
                                reference_name = value.get("smc-reference")
                                if reference_name is not None:
                                    result = fetch_meta_by_name(reference_name)
                                    if len(result.json) == 0:
                                        self.fail(msg="reference {} not found".format(value))
                                    value = result.json[0].get("href")
                                    logger.debug("Updated: reference found={}".format(value))
                            if type(value) is list:
                                value_list = []
                                for sub_value in value.copy():
                                    logger.debug("Updated: sub-value={}".format(sub_value))
                                    if type(sub_value) is dict:
                                        reference_name = sub_value.get("smc-reference")
                                        if reference_name is not None:
                                            result = fetch_meta_by_name(reference_name)
                                            if len(result.json) == 0:
                                                self.fail(msg="reference {} not found".format(value))
                                            sub_value = result.json[0].get("href")
                                            logger.debug("Updated: reference found in list={}".format(sub_value))
                                    value_list.append(sub_value)
                                value = value_list

                            json_payload[attribute] = value

                        instance, updated, created = lookup_class(typeof).update_or_create(
                            with_status=True, **json_payload)
                        logger.debug("instance={} updated={} created={}".format(instance, updated, created))

                        action = 'none'

                        if updated:
                            action = 'updated'
                        elif created:
                            action = 'created'

                        if updated or created:
                            self.results['changed'] = True

                        self.results['state'].append(dict(name=instance.name,
                            typeof=instance.typeof, action=action))

                    except SMCException as e:
                        logger.error("Exception={}".format(str(e)))
                        self.results['state'].append(dict(name=data.get('name'),
                            typeof=typeof, action='error', reason=str(e)))

        except SMCException as err:
            self.fail(msg=str(err), exception=traceback.format_exc())

        logger.debug("result={}".format(self.results))
        return self.results


def main():
    GenericElement()


if __name__ == '__main__':
    main()
