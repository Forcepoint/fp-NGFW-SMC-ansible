# fp-NGFW-SMC-ansible

This repository provides [Ansible](https://www.ansible.com)  modules for configuration and automation of [Forcepoint NGFW Next Generation Firewall](https://www.forcepoint.com/product/network-security/forcepoint-ngfw). 
It uses the [fp-NGFW-SMC-python](https://github.com/Forcepoint/fp-NGFW-SMC-python) for all operations between the ansible client 
and the Forcepoint NGFW Management Center.

## Prerequisites

* fp-NGFW-SMC-python >= 1.0.24
* Forcepoint NGFW Management Center >= 6.10.x
* API client account with permissions

## Installation

### Using `virtualenv` (recommended)
```
pip install ansible
git clone https://github.com/Forcepoint/fp-NGFW-SMC-ansible.git
cd fp-NGFW-SMC-ansible
pip install -r requirements.txt
```

Once installed, there is a helper script `install.py` that will copy the fp-NGFW-SMC-ansible docs and module_util into the ansible directories:

```
python install.py
```

* Enable the SMC API within the management center

## Usage

Each ansible run will require a login event to the Forcepoint NGFW Management Center to perform it's operations.
Since the ansible libraries use smc-python, the login process uses the same session logic.

* You can provide url and api_key as task parameters
* You can provide the `smc_alt_filepath` parameter in the task run to specify where to find the .smcrc file with your stored credentials

If neither of the two above are used, then:
* Try to find ~.smcrc in users home directory
* Use environment variables (SMC_ADDRESS, SMC_API_KEY, ...)


### 🧪 Example Using Environment Variables and a Python Virtual Environment

Here is an example of how to use environment variables along with a Python virtual environment:

```
# Create and activate a virtual environment
cd stonesoft-ansible
python3 -m venv venv
source venv/bin/activate

# Export environment variables
export ANSIBLE_LIBRARY=library
export ANSIBLE_CONFIG=ansible.cfg
export SMC_ADDRESS=https://localhost:8082
export SMC_API_KEY=HuphG4Uwg4dN6TyvorTR0001

# Run your playbook
ansible-playbook -v playbooks/example.yml

```

If none of the above succeed, the run will fail. 

## Running playbooks

Before running plays, it's best to explain the architecture used to make the administrative changes. 


The Forcepoint NGFW Management Center is where modifications to all elements are performed.

Installing the ansible modules can therefore either be done on a client host machine remote from the SMC, or on the SMC itself.

If the ansible modules are installed on a controller that is remote from the SMC, set your inventory to use localhost for the connection. 

For example, set your default inventory */etc/ansible/hosts*:
```
localhost ansible_connection=local
```
Note that the host running the ansible client will still need to connect to the SMC through the smc-python API over the default port 8082/tcp.

The other option is to install the ansible libraries on the SMC server itself and make your ansible runs from the controller client. 
In this case, the SMC connection can then be done using an SMC url of 127.0.0.1.

### 🔁 Playbook Execution Order

Some playbooks need to be executed in a specific order, as certain ones create network elements required by others. Typically, `network_element.yml` and `element.yml` should be run first.

Below is a coherent scenario for creating and configuring a firewall:

```
ansible-playbook -v playbooks/network_element.yml
ansible-playbook -v playbooks/element.yml
ansible-playbook -v playbooks/anypolicy.yml
ansible-playbook -v playbooks/l3fw.yml
ansible-playbook -v playbooks/l3fw_add_interface.yml
ansible-playbook -v playbooks/engine_routing.yml
ansible-playbook -v playbooks/engine_action.yml
```
## More information

All modules provide doc snippets when run from the ansible client:

```
ansible-doc -s engine
```

## Contributing

Thank you for considering contributing to our project! To ensure code consistency and quality, we use several tools for code validation and formatting. 
Below are the steps to validate and auto-format your code.

## Documentation

[View Documentation on Read The Docs](https://fp-ngfw-smc-ansible.readthedocs.io/en/latest/?badge=latest)
