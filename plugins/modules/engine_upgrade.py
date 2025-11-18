#!/usr/bin/python
# Copyright (c) 2025 Forcepoint

import logging
import traceback

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: engine_upgrade
short_description: Download and activate upgrade packages for engines

description:
  - This module downloads and activates engine upgrade packages on specified engine nodes.
  - If the upgrade package is not already downloaded, it will be downloaded before activation.

version_added: '2.5'

options:
  name:
    description:
      - Name of the engine to upgrade
    type: str
    required: true
  upgrade_version:
    description:
      - Version of the engine upgrade package to download and activate
      - Specify the version in format '6.10.15' to get the latest build of that version
    type: str
    required: true
  engine_nodes:
    description:
      - List of engine node IDs to activate the upgrade on
      - If not specified, will try to upgrade all nodes of the engine
    type: list
    elements: int
    required: false
  wait_for_finish:
    description:
      - Whether to wait for the download/activation to complete before returning
    type: bool
    default: true
  wait_time:
    description:
      - Time in seconds to wait between polling for task completion status
    type: int
    default: 5

extends_documentation_fragment: management_center

notes:
  - Login credential information is either obtained by providing them directly
    to the task/play, specifying an alt_filepath to read the credentials from to
    the play, or from environment variables (in that order).
  - This module requires smc-python with engine upgrade capabilities.

requirements:
  - smc-python
author:
  - Forcepoint
'''

EXAMPLES = '''
- name: Download and activate engine upgrade package
  hosts: localhost
  gather_facts: no
  tasks:
  - name: Upgrade engine
    engine_upgrade:
      name: myengine
      upgrade_version: '6.10.15'
      engine_nodes: [1, 2]
      wait_for_finish: true
      wait_time: 10
'''

RETURN = '''
msg:
    description: Status message from the operation
    returned: always
    type: str
    sample: "Engine upgrade 6.10.15 has been activated on myengine"
download_status:
    description: Status of the download operation
    returned: always
    type: dict
    sample: {
        "progress": 100,
        "success": true,
        "last_message": "Download completed successfully"
    }
activation_status:
    description: Status of the activation operation
    returned: always
    type: dict
    sample: {
        "progress": 100,
        "success": true,
        "last_message": "Activation completed successfully"
    }
'''

from ansible_collections.forcepoint.fp_ngfw_smc_ansible.plugins.module_utils.smc_util import ForcepointModuleBase

try:
    from smc.core.engine import Engine
    from smc.api.exceptions import SMCException
    from smc.administration.system import System
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("smc")

class RemoteUpgradeError(Exception):
    pass

def get_system():
    return System()

def get_engine_nodes_href(engine_name, node_ids=None):
    """
    Get the href list for engine nodes, filtered by node_ids if provided.
    Args:
        engine_name (str): The name of the engine
        node_ids (list, optional): List of node IDs (1-based) to include. If None, all nodes are returned.
    Returns:
        list: List of node href strings
    """
    nodes_href_list = []
    engine = Engine(engine_name)
    for idx, node in enumerate(engine.nodes, 1):  # 1-based node IDs
        if node_ids is None or idx in node_ids:
            nodes_href_list.append(node.href)
    return nodes_href_list

class EngineUpgrade(ForcepointModuleBase):
    def __init__(self):
        self.module_args = dict(
            name=dict(type='str', required=True),
            upgrade_version=dict(type='str', required=True),
            engine_nodes=dict(type='list', elements='int', required=False),
            wait_for_finish=dict(type='bool', default=True),
            wait_time=dict(type='int', default=5)
        )
        self.results = dict(
            changed=False,
            msg=''
        )
        super(EngineUpgrade, self).__init__(self.module_args, supports_check_mode=False)

    def exec_module(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        try:
            self.download_and_activate_upgrade()
        except RemoteUpgradeError as err:
            self.fail(msg=str(err))
        except SMCException as err:
            self.fail(msg=str(err), exception=traceback.format_exc())
        return self.results

    def download_and_activate_upgrade(self):
        # Use self.engine_nodes if provided, else None
        node_ids = getattr(self, 'engine_nodes', None)
        engine_nodes_list = get_engine_nodes_href(self.name, node_ids)
        logger.info("Engine nodes href list: %s", engine_nodes_list)
        _sys = get_system()
        upgrades = _sys.engine_upgrade()
        package = upgrades.get_contains(self.upgrade_version)
        if not package:
            raise RemoteUpgradeError("Upgrade package for the given engine version not found.")
        # Download if needed
        try:
            is_downloaded = False
            try:
                if package.data["link"][1]["rel"] == "activate":
                    is_downloaded = True
            except KeyError:
                pass
            if not is_downloaded:
                logger.info(f"Downloading engine upgrade %s ...", self.upgrade_version)
                poller = package.download(wait_for_finish=True)
                while not poller.done():
                    logger.info(f"Download of engine upgrade %s in progress ...", self.upgrade_version)
                    poller.wait(self.wait_time)
                logger.info(poller.last_message())
                if not poller.is_success():
                    logger.error(f"An error happened while downloading the remote upgrade - %s", poller.task.last_message)
                    raise RemoteUpgradeError(f"An error happened while downloading the remote upgrade - {poller.task.last_message}")
                self.results['changed'] = True
                self.results['download_status'] = {
                    "progress": poller.task.progress,
                    "success": poller.is_success(),
                    "last_message": poller.last_message()
                }
            else:
                logger.info(f"Engine upgrade %s is already downloaded", self.upgrade_version)
                self.results['download_status'] = {
                    "progress": 100,
                    "success": True,
                    "last_message": "Package already downloaded"
                }
        except Exception as e:
            logger.error(f"Failed to download package: {str(e)}")
            raise RemoteUpgradeError(f"Failed to download package: {str(e)}")
        # Activate
        try:
            logger.info(f"Activating engine upgrade %s on %s...", self.upgrade_version, self.name)
            upgrades = _sys.engine_upgrade()
            package = upgrades.get_contains(self.upgrade_version)
            poller = package.activate(engine_nodes_list, wait_for_finish=True)
            while not poller.done():
                logger.info(f"Percentage complete %s%%", poller.task.progress)
                poller.wait(self.wait_time)
            logger.info(poller.last_message())
            if not poller.is_success():
                logger.error(f"An error happened during remote upgrade - %s", poller.task.last_message)
                raise RemoteUpgradeError(f"An error happened during remote upgrade - {poller.task.last_message}")
            self.results['changed'] = True
            self.results['activation_status'] = {
                "progress": poller.task.progress,
                "success": poller.is_success(),
                "last_message": poller.last_message()
            }
            self.results['msg'] = f"Engine upgrade {self.upgrade_version} has been activated on {self.name}"
        except Exception as e:
            logger.error(f"Failed to activate package: %s", str(e))
            raise RemoteUpgradeError(f"Failed to activate package: %s", str(e))

def main():
    EngineUpgrade()

if __name__ == '__main__':
    main()
