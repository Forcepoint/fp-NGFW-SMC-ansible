#!/usr/bin/python
# Copyright (c) 2026 Forcepoint
import logging
import traceback

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: engine_user_authentication_certificate
short_description: Manage user authentication certificate operations on an engine

description:
  - Exposes the user authentication certificate operations provided by smc-python.
  - Operations are intentionally atomic so certificate requests can be signed by an
    external signing workflow before the signed certificate is imported.
  - The module returns certificate request and certificate content under a C(content) key
    and does not require controller-side files.
  - Export operations return C(content=null) when no certificate request or certificate
    is available.

version_added: '1.0.9'

options:
  name:
    description:
      - Name of the engine on which to perform the certificate operation.
    type: str
    required: true
  action:
    description:
      - Atomic user authentication certificate operation to perform.
      - C(export_request) and C(export_certificate) are read-only operations and can be used
        to determine whether a certificate request or certificate is available.
      - C(generate_request) does not delete an existing certificate request implicitly.
    type: str
    required: true
    choices:
      - delete_request
      - generate_request
      - export_request
      - import_certificate
      - export_certificate
      - delete_certificate
      - generate_and_sign_certificate
  certificate:
    description:
      - PEM encoded certificate content to import.
      - Required when I(action=import_certificate).
      - The private key is generated and retained by the engine and must not be provided.
    type: str
  extra_args:
    description:
      - Optional keyword arguments passed to the corresponding smc-python Engine method.
      - This preserves compatibility with SMC versions that expose additional method options.
      - Do not use this option to provide the certificate for C(import_certificate); use
        I(certificate) instead.
    type: dict
    default: {}

extends_documentation_fragment: management_center

notes:
  - The external signing workflow is deliberately outside this module.
  - C(generate_request) and C(generate_and_sign_certificate) are imperative operations
    and report C(changed=true) when executed.
  - Login credential information is obtained from task parameters, an alternate SMC
    configuration file, or environment variables as supported by the collection.

requirements:
  - smc-python

author:
  - Forcepoint
'''

EXAMPLES = r'''
- name: Delete the previous pending certificate request
  forcepoint.fp_ngfw_smc_ansible.engine_user_authentication_certificate:
    name: firewall01
    action: delete_request

- name: Generate a new certificate request
  forcepoint.fp_ngfw_smc_ansible.engine_user_authentication_certificate:
    name: firewall01
    action: generate_request

- name: Export the certificate request as content
  forcepoint.fp_ngfw_smc_ansible.engine_user_authentication_certificate:
    name: firewall01
    action: export_request
  register: user_authentication_csr

- name: Generate a request when none is available
  forcepoint.fp_ngfw_smc_ansible.engine_user_authentication_certificate:
    name: firewall01
    action: generate_request
  when: user_authentication_csr.csr.content is none

- name: Import the certificate signed by an external CA
  forcepoint.fp_ngfw_smc_ansible.engine_user_authentication_certificate:
    name: firewall01
    action: import_certificate
    certificate: "{{ signed_certificate }}"

- name: Export the currently installed certificate
  forcepoint.fp_ngfw_smc_ansible.engine_user_authentication_certificate:
    name: firewall01
    action: export_certificate
  register: installed_user_authentication_certificate
'''

RETURN = r'''
changed:
  description: Whether the engine configuration was changed.
  returned: always
  type: bool
engine:
  description: Name of the engine on which the operation was performed.
  returned: always
  type: str
action:
  description: Certificate operation that was performed.
  returned: always
  type: str
csr:
  description: Certificate request export result.
  returned: when action is export_request
  type: dict
  contains:
    content:
      description:
        - PEM encoded certificate request content.
        - C(null) when no certificate request is available.
      type: str
certificate:
  description: Installed certificate export result.
  returned: when action is export_certificate
  type: dict
  contains:
    content:
      description:
        - PEM encoded installed certificate content.
        - C(null) when no certificate is available.
      type: str
msg:
  description: Result returned by smc-python for mutating operations.
  returned: when provided by smc-python
  type: raw
'''

from ansible_collections.forcepoint.fp_ngfw_smc_ansible.plugins.module_utils.smc_util import ForcepointModuleBase, allowed_args

try:
    from smc.core.engine import Engine
    from smc.api.exceptions import SMCException
except ImportError:
    pass


logger = logging.getLogger("smc")

ACTIONS = (
    'delete_request',
    'generate_request',
    'export_request',
    'import_certificate',
    'export_certificate',
    'delete_certificate',
    'generate_and_sign_certificate'
)

METHODS = {
    'delete_request': 'delete_user_authentication_certificate_request',
    'generate_request': 'generate_user_authentication_certificate_request',
    'export_request': 'export_user_authentication_certificate_request',
    'import_certificate': 'user_authentication_import_certificate',
    'export_certificate': 'export_user_authentication_certificate',
    'delete_certificate': 'delete_user_authentication_certificate',
    'generate_and_sign_certificate': 'generate_and_sign_user_authentication_certificate'
}

READ_ONLY_ACTIONS = ('export_request', 'export_certificate')


class ForcepointEngineUserAuthenticationCertificate(ForcepointModuleBase):
    def __init__(self):
        self.module_args = dict(
            name=dict(type='str', required=True),
            action=dict(type='str', required=True, choices=ACTIONS),
            certificate=dict(type='str', required=False),
            extra_args=dict(type='dict', default={}))

        self.certificate = None
        self.extra_args = None

        self.results = dict(
            changed=False,
            engine=None,
            action=None)

        required_if = [
            ('action', 'import_certificate', ('certificate',))
        ]

        super(ForcepointEngineUserAuthenticationCertificate, self).__init__(
            self.module_args,
            required_if=required_if,
            supports_check_mode=True)

    def exec_module(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

        self.results['engine'] = self.name
        self.results['action'] = self.action

        try:
            engine = Engine(self.name)
            method_name = METHODS[self.action]
            method = getattr(engine, method_name, None)
            if method is None:
                self.fail(msg='The installed smc-python version does not provide Engine.%s' % method_name)

            self.check_provided_args(engine, method_name)

            if self.check_mode and self.action not in READ_ONLY_ACTIONS:
                self.results['changed'] = True
                return self.results

            if self.action == 'import_certificate':
                result = method(self.certificate, **self.extra_args)
            else:
                result = method(**self.extra_args)

            if self.action == 'export_request':
                self.results['csr'] = self.build_content_result(result)
            elif self.action == 'export_certificate':
                self.results['certificate'] = self.build_content_result(result)
            else:
                self.results['changed'] = True
                if result is not None:
                    self.results['msg'] = result

        except SMCException as err:
            self.fail(msg=str(err), exception=traceback.format_exc())
        except (AttributeError, TypeError, ValueError) as err:
            self.fail(msg=str(err), exception=traceback.format_exc())

        return self.results

    def check_provided_args(self, engine, operation):
        allowed = allowed_args(engine, operation)
        for arg in self.extra_args:
            if arg not in allowed:
                self.fail(msg='Invalid argument provided to engine operation %r. Valid arguments '
                    'for this operation are %s' % (arg, allowed))

    @staticmethod
    def build_content_result(content):
        if content is None:
            return {'content': None}
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        content = str(content)
        return {'content': content if content.strip() else None}


def main():
    ForcepointEngineUserAuthenticationCertificate()


if __name__ == '__main__':
    main()
