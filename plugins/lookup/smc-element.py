from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from smc import session
from smc.api.common import fetch_meta_by_name
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from smc.base.model import Element

DOCUMENTATION = """
    lookup: smc-element
    author: Forcepoint
    version_added: 
    short_description: Lookup smc-python Element object from a smc element name
    description:
      - Retrieves the Element for a given SMC element name.
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
            href = found.json[0].get("href")
            print("found={}".format(href))
            return [Element.from_href(href)]
        except BaseException as e:
            raise AnsibleError("smc-element error: {}".format(e))
