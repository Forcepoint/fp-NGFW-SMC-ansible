#######
Modules
#######

Modules provide the functionality to add, modify, and remove elements within the SMC. Each module focuses on a specific
functionality, allowing playbooks to be designed in a modular way. Not all modules provide the ability to modify elements. Be sure to review the documentation. 

There are a variety of functions provided by the custom modules. Some of the features include:

* Create Firewalls and Firewall Clusters
* Add / Remove Tunnel and Physical Interfaces
* Create and delete network and service elements
* Configure Policy-based VPN and related elements
* Configure dynamic routing (BGP)

Modules by default will preset the state to 'present' indicating a create operation. To remove, modify the state to 'absent'. 

When modules are run, the `state` attribute will return the current state of the element. Check the module documentation to verify if this is a dict format or list.

.. toctree::
   :glob:
   
   *

