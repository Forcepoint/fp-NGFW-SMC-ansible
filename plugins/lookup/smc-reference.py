from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from smc import session
from smc.api.common import fetch_meta_by_name
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

DOCUMENTATION = """
    lookup: smc-reference
    author: Forcepoint
    version_added: 
    short_description: Lookup reference for a smc element
    description:
      - Retrieves the reference for a SMC element for the given name.
      - needs to set login data to connect to SMC:
        -  "export SMC_ADDRESS=http://localhost:8082"
        -  "export SMC_API_KEY=MaJ3n8ExWBh4njHDv9EaucCX"
    options:
      _terms:
        description: The element name to look up
        required: True
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        try:
            session.login()
            print("terms={}".format(terms))
            found = fetch_meta_by_name(terms[0])
            print("found={}".format(found))
            if len(found.json) == 0:
                raise AnsibleError("can't find element {}".format(terms))
            return [found.json[0].get("href")]
        except BaseException as e:
            raise AnsibleError("smc-reference error: {}".format(e))
