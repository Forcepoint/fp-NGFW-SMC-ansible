#!/usr/bin/python
# -*- coding: utf-8 -*-
# Apache-2.0

DOCUMENTATION = r'''
---
module: engine_session_monitoring
short_description: Retrieve session monitoring facts for a Forcepoint NGFW Engine
description:
  - Read-only facts module that queries Forcepoint NGFW Engine session monitoring via the SMC API.
version_added: "1.0.8"
author:
  - "Forcepoint"
requirements:
  - fp-NGFW-SMC-python >= 1.0.31
notes:
  - This module does not modify any state; it always returns C(changed=false).
  - Authentication can be provided explicitly (task params) or via environment variables / .smcrc (handled by the base class).
  - To enable API call logging, use C(smc_logging) (handled by the base class).
options:
  filter:
    description: Engine name to query (exact or substring match).
    type: str
    required: true
  exact_match:
    description: Require an exact match on engine name.
    type: bool
    default: false
  case_sensitive:
    description: Case sensitivity for substring match when C(exact_match=false).
    type: bool
    default: true
  sesmon_type:
    description:
      - Session Monitoring type to retrieve.
      - Supported values: C(routing_monitoring), C(connection_monitoring),
        C(blocklist_monitoring), C(user_monitoring), C(vpnsa_monitoring),
        C(sslvpn_monitoring), C(neighbor_monitoring).
    type: str
    required: true
    choices:
      - routing_monitoring
      - connection_monitoring
      - blocklist_monitoring
      - user_monitoring
      - vpnsa_monitoring
      - sslvpn_monitoring
      - neighbor_monitoring
  full:
    description:
      - Pass-through to the Python API call C(get_session_monitoring).
      - When true (default), the API returns the full default field set for the monitor.
    type: bool
    default: true

extends_documentation_fragment:
  - management_center
  - management_center_facts
'''

EXAMPLES = r'''
- name: Retrieve connection monitoring for engine "Plano"
  engine_session_monitoring:
    filter: Plano
    sesmon_type: connection_monitoring

- name: Retrieve neighbor monitoring (exact match, case-insensitive)
  engine_session_monitoring:
    filter: plano
    sesmon_type: neighbor_monitoring
    exact_match: true
    case_sensitive: false

- name: Use .smcrc and enable API logging
  engine_session_monitoring:
    filter: dc-fw
    sesmon_type: vpnsa_monitoring
    smc_alt_filepath: /home/ansible/.smcrc
    smc_logging:
      path: ansible-smc.log
      level: 10
'''

RETURN = r'''
ansible_facts:
  description: Monitoring facts
  returned: always
  type: dict
  contains:
    engine_session_monitoring:
      description: Structured monitoring result
      type: dict
      contains:
        engine:
          description: Resolved engine name used for the query.
          type: str
        sesmon_type:
          description: The monitoring type requested.
          type: str
        full:
          description: Whether 'full' was used in the API call.
          type: bool
        is_all:
          description: Whether all entries were returned (SessionMonitoringResult.isAll).
          type: bool
        count:
          description: Number of returned items (derived).
          type: int
        items:
          description: Monitoring items (JSON-serializable).
          type: raw
changed:
  description: Always false; read-only module.
  type: bool
  returned: always
'''

from ansible.module_utils.smc_util import ForcepointModuleBase  # provided by this collection
from ansible.module_utils.six import string_types

SUPPORTED_TYPES = {
    "routing_monitoring",
    "connection_monitoring",
    "blocklist_monitoring",
    "user_monitoring",
    "vpnsa_monitoring",
    "sslvpn_monitoring",
    "neighbor_monitoring",
}

def _engine_match(name, needle, exact, case_sensitive):
    if exact:
        return name == needle if case_sensitive else name.lower() == needle.lower()
    # substring
    return (needle in name) if case_sensitive else (needle.lower() in name.lower())

def _to_jsonable(obj):
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool, dict, list)):
        return obj
    if isinstance(obj, tuple):
        return list(obj)
    # common adapters
    for m in ('to_dict', 'as_dict', 'to_json', 'as_json'):
        fn = getattr(obj, m, None)
        if callable(fn):
            try:
                return _to_jsonable(fn())
            except Exception:
                pass
    try:
        return [_to_jsonable(x) for x in obj]
    except Exception:
        pass
    return str(obj)

def _unwrap_session_monitoring_result(obj):
    """
    Recognize smc.core.session_monitoring.SessionMonitoringResult and normalize it.
    (Duck-typing to avoid a hard import dependency here.)
    """
    try:
        if hasattr(obj, 'sesmon_type') and hasattr(obj, 'result') and hasattr(obj, 'isAll'):
            return {
                'sesmon_type': getattr(obj, 'sesmon_type'),
                'is_all': bool(getattr(obj, 'isAll')),
                'result': _to_jsonable(getattr(obj, 'result'))
            }
    except Exception:
        pass
    return None


class EngineSessionMonitoringFacts(ForcepointModuleBase):
    """
    Facts module retrieving Engine session monitoring using:
      Engine.get_session_monitoring(sesmon_type, full=...)
    """

    def __init__(self):
        # Module-specific args (base class injects SMC auth/logging/facts args)
        module_args = dict(
            filter=dict(type='str', required=True),
            exact_match=dict(type='bool', default=False),
            case_sensitive=dict(type='bool', default=True),
            sesmon_type=dict(type='str', required=True, choices=sorted(SUPPORTED_TYPES)),
            full=dict(type='bool', default=True),
        )

        # Attributes consumed in exec_module
        self.filter = None
        self.exact_match = None
        self.case_sensitive = None
        self.sesmon_type = None
        self.full = None

        # Result envelope (facts-style)
        self.results = dict(
            changed=False,
            ansible_facts=dict(
                engine_session_monitoring={}
            )
        )

        super(EngineSessionMonitoringFacts, self).__init__(module_args, is_fact=True)

    def exec_module(self, **kwargs):
        """
        Called by the base class after it initializes auth, logging, etc.
        """
        for name, value in kwargs.items():
            setattr(self, name, value)

        # Lazy import (so ansible-doc works even if fp-NGFW-SMC-python isn't installed locally)
        try:
            from smc.core.engine import Engine
        except ImportError as e:
            self.fail(msg="fp-NGFW-SMC-python is not installed or not importable: {}".format(e))

        # Resolve engine by name
        engine_obj = None
        if self.exact_match:
            try:
                candidate = Engine(self.filter)
                _ = candidate.href  # force resolution
                engine_obj = candidate
            except Exception:
                self.fail(msg="Engine not found (exact_match): {}".format(self.filter))
        else:
            matches = []
            for eng in Engine.objects.all():
                name = getattr(eng, 'name', str(eng))
                if _engine_match(name, self.filter, False, self.case_sensitive):
                    matches.append(eng)
            if not matches:
                self.fail(msg="No engine matched filter '{}'".format(self.filter))
            if len(matches) > 1:
                names = [getattr(e, 'name', str(e)) for e in matches]
                self.fail(msg="Multiple engines matched '{}': {}. Use exact_match or refine filter."
                               .format(self.filter, names))
            engine_obj = matches[0]

        # Check mode: read-only preview
        if self.module.check_mode:
            self.results['ansible_facts']['engine_session_monitoring'] = dict(
                engine=getattr(engine_obj, 'name', self.filter),
                sesmon_type=self.sesmon_type,
                full=bool(self.full),
                is_all=None,
                count=0,
                items=[]
            )
            return self.results

        # Actual monitoring call
        # Engine.get_session_monitoring is provided by smc-python Engine API.
        data = engine_obj.get_session_monitoring(self.sesmon_type, full=bool(self.full))

        # Normalize SessionMonitoringResult -> dict
        unwrapped = _unwrap_session_monitoring_result(data)
        if unwrapped is not None:
            items = unwrapped['result']
            is_all = unwrapped['is_all']
            sesmon_type_out = unwrapped['sesmon_type'] or self.sesmon_type
        else:
            items = _to_jsonable(data)
            is_all = None
            sesmon_type_out = self.sesmon_type

        # Count
        if isinstance(items, list):
            count = len(items)
        elif isinstance(items, dict):
            count = len(items) if items else 0
        else:
            count = 1 if items is not None else 0

        self.results['ansible_facts']['engine_session_monitoring'] = dict(
            engine=getattr(engine_obj, 'name', self.filter),
            sesmon_type=sesmon_type_out,
            full=bool(self.full),
            is_all=is_all,
            count=count,
            items=items
        )
        return self.results


def main():
    EngineSessionMonitoringFacts()


if __name__ == '__main__':
    main()
