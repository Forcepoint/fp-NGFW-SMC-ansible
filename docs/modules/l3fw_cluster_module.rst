.. _l3fw_cluster:


l3fw_cluster - Create or delete firewall clusters
+++++++++++++++++++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2

DEPRECATED
----------

:In: version: 
:Why: Replaced with single module
:Alternative: :ref:`engine <engine>`



Synopsis
--------


* Firewall clusters can be created with up to 16 nodes per cluster. Each cluster_node specified will define a unique cluster member and dictate the number of cluster nodes. You can fetch an existing engine using engine_facts and optionally save this as YAML to identify differences between runs. Interfaces and VLANs can be added, modified or removed. By default if the interface is not defined in the YAML, but exists on the engine, it will be deleted. To change an interface ID or VLAN id, you must delete the old and recreate the new interface definition. In addition, it is not possible to modify interfaces that have multiple IP addresses defined (they will be skipped).



Requirements (on host that executes module)
-------------------------------------------

  * smc-python


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>antivirus<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td><ul><li>yes</li><li>no</li></ul></td>
	<td>
        <p>Enable Anti-Virus engine on the firewall</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>backup_mgt<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>(Cluster only) Specify an interface by ID that will be the backup heartbeat interface. For VLAN, specify the interface ID in dot syntax. For example, 1.2 indicates interface 1, VLAN 2.</p>
	</td>
	</tr>
    </td>
    </tr>
    <tr>
    <td rowspan="2">bgp<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>If enabling BGP on the engine, provide BGP-related settings.</div>
    </tr>

    <tr>
    <td colspan="5">
        <table border=1 cellpadding=4>
        <caption><b>Dictionary object bgp</b></caption>

        <tr>
        <th class="head">parameter</th>
        <th class="head">required</th>
        <th class="head">default</th>
        <th class="head">choices</th>
        <th class="head">comments</th>
        </tr>

        <tr>
        <td>router_id<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>Optional router ID to identify this BGP peer</div>
        </td>
        </tr>

        <tr>
        <td>bgp_peering<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>BGP Peerings to add to specified interfaces.</div>
        </td>
        </tr>

        <tr>
        <td>announced_network<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td><ul><li>network</li><li>group</li><li>host</li></ul></td>
        <td>
            <div>Announced networks identify the network and optional route map for internal networks announced over BGP. The list should be a dict with the key identifying the announced network type from SMC. The key should have a dict with name and route_map (optional) if the element should have an associated route_map.</div>
        </td>
        </tr>

        <tr>
        <td>antispoofing_network<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td><ul><li>network</li><li>group</li><li>host</li></ul></td>
        <td>
            <div>Antispoofing networks are automatically added to the route antispoofing configuration. The dict should have a key specifying the element type from SMC. The dict key value should be a list of the element types by name.</div>
        </td>
        </tr>

        <tr>
        <td>enabled<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td>
            <div>Set to true or false to specify whether to configure BGP</div>
        </td>
        </tr>

        <tr>
        <td>autonomous_system<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>The autonomous system for this engine. Provide additional arguments to allow for get or create logic</div>
        </td>
        </tr>

        </table>

    </td>
    </tr>
    </td>
    </tr>

    <tr>
    <td>cluster_mode<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>standby</td>
    <td><ul><li>balancing</li><li>standby</li></ul></td>
	<td>
        <p>How to perform clustering: load-balancing or standby</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>comment<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Optional comment tag for the engine</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>default_nat<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td><ul><li>yes</li><li>no</li></ul></td>
	<td>
        <p>Whether to enable default NAT on the firewall. Default NAT will identify internal networks and use the external interface IP for outgoing traffic</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>delete_undefined_interfaces<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td><ul><li>yes</li><li>no</li></ul></td>
	<td>
        <p>Delete interfaces that are not defined in the YAML file from the NGFW Engine. This parameter can be used as a strategy to remove interfaces. One option is to retrieve the full engine json using engine_facts as YAML, then remove the interfaces from the YAML and set delete_undefined_interfaces to yes.</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>domain_server_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>A list of IP addresses to use as DNS resolvers for the firewall. Required to enable Antivirus, GTI and URL Filtering on the NGFW.</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>file_reputation<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td><ul><li>yes</li><li>no</li></ul></td>
	<td>
        <p>Enable file reputation</p>
	</td>
	</tr>
    </td>
    </tr>
    <tr>
    <td rowspan="2">interfaces<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
    <td></td>
    <td>
        <div>Define the interface settings for this cluster interface, such as address, network and node id.</div>
    </tr>

    <tr>
    <td colspan="5">
        <table border=1 cellpadding=4>
        <caption><b>Dictionary object interfaces</b></caption>

        <tr>
        <th class="head">parameter</th>
        <th class="head">required</th>
        <th class="head">default</th>
        <th class="head">choices</th>
        <th class="head">comments</th>
        </tr>

        <tr>
        <td>comment<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>Optional comment for this interface. If you want to unset the interface comment, set to an empty string or define with no value.</div>
        </td>
        </tr>

        <tr>
        <td>macaddress<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>The mac address to assign to the cluster virtual IP interface. This is required if the <em>cluster_virtual</em> parameter is defined</div>
        </td>
        </tr>

        <tr>
        <td>zone_ref<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>Optional zone name for this interface</div>
        </td>
        </tr>

        <tr>
        <td>network_value<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>The cluster netmask for the cluster_vip. Required if the <em>cluster_virtual</em> parameter is defined</div>
        </td>
        </tr>

        <tr>
        <td>cluster_virtual<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>The cluster virtual (shared) IP address for all cluster members. Not required if only creating NDIs</div>
        </td>
        </tr>

        <tr>
        <td>nodes<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>List of the nodes for this interface</div>
        </td>
        </tr>

        <tr>
        <td>interface_id<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>The cluster NIC ID for this interface. Required.</div>
        </td>
        </tr>

        </table>

    </td>
    </tr>
    </td>
    </tr>

    <tr>
    <td>location<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Location identifier for the engine. Used when engine is behind NAT. If a location is set on the engine and you want to reset to unspecified, then use the keyword None.</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
    <td></td>
	<td>
        <p>The name of the firewall cluster to add or delete</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>primary_heartbeat<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Specify an interface for the primary heartbeat interface. This will default to the same interface as primary_mgt if not specified.</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>primary_mgt<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
    <td></td>
	<td>
        <p>Identify the interface to be specified as management. When creating a new cluster, the primary mgt must be a non-VLAN interface. You can move it to a VLAN interface after creation.</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>skip_interfaces<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td><ul><li>yes</li><li>no</li></ul></td>
	<td>
        <p>Optionally skip the analysis of interface changes. This is only relevant when running the playbook against an already created engine. This must be false if attempting to add interfaces.</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>smc_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>FQDN with port of SMC. The default value is the environment variable <code>SMC_ADDRESS</code></p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>smc_alt_filepath<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Provide an alternate path location to read the credentials from. File is expected to be stored in ~.smcrc. If provided, url and api_key settings are not required and will be ignored.</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>smc_api_key<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>API key for api client. The default value is the environment variable <code>SMC_API_KEY</code> Required if <em>url</em></p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>smc_api_version<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Optional API version to connect to. If none is provided, the latests LTS SMC API version will be used based on the Management Center version. Can be set though the environment variable <code>SMC_API_VERSION</code></p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>smc_domain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Optional domain to log in to. If no domain is provided, 'Shared Domain' is used. Can be set throuh the environment variable <code>SMC_DOMAIN</code></p>
	</td>
	</tr>
    </td>
    </tr>
    <tr>
    <td rowspan="2">smc_extra_args<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>Extra arguments to pass to login constructor. These are generally only used if specifically requested by support personnel.</div>
    </tr>

    <tr>
    <td colspan="5">
        <table border=1 cellpadding=4>
        <caption><b>Dictionary object smc_extra_args</b></caption>

        <tr>
        <th class="head">parameter</th>
        <th class="head">required</th>
        <th class="head">default</th>
        <th class="head">choices</th>
        <th class="head">comments</th>
        </tr>

        <tr>
        <td>verify<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td>
            <div>Is the connection to SMC is HTTPS, you can set this to True, or provide a path to a client certificate to verify the SMC SSL certificate. You can also explicitly set this to False.</div>
        </td>
        </tr>

        </table>

    </td>
    </tr>
    </td>
    </tr>
    <tr>
    <td rowspan="2">smc_logging<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>Optionally enable SMC API logging to a file</div>
    </tr>

    <tr>
    <td colspan="5">
        <table border=1 cellpadding=4>
        <caption><b>Dictionary object smc_logging</b></caption>

        <tr>
        <th class="head">parameter</th>
        <th class="head">required</th>
        <th class="head">default</th>
        <th class="head">choices</th>
        <th class="head">comments</th>
        </tr>

        <tr>
        <td>path<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>Full path to the log file</div>
        </td>
        </tr>

        <tr>
        <td>level<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>Log level as specified by the standard python logging library, in int format. Default setting is logging.DEBUG.</div>
        </td>
        </tr>

        </table>

    </td>
    </tr>
    </td>
    </tr>

    <tr>
    <td>smc_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Optional timeout for connections to the SMC. Can be set through environment <code>SMC_TIMEOUT</code></p>
	</td>
	</tr>
    </td>
    </tr>
    <tr>
    <td rowspan="2">snmp<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>SNMP settings for the engine</div>
    </tr>

    <tr>
    <td colspan="5">
        <table border=1 cellpadding=4>
        <caption><b>Dictionary object snmp</b></caption>

        <tr>
        <th class="head">parameter</th>
        <th class="head">required</th>
        <th class="head">default</th>
        <th class="head">choices</th>
        <th class="head">comments</th>
        </tr>

        <tr>
        <td>snmp_agent<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>The name of the SNMP agent from within the SMC</div>
        </td>
        </tr>

        <tr>
        <td>enabled<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td>
            <div>Set this to False if enabled on the engine and wanting to remove the configuration.</div>
        </td>
        </tr>

        <tr>
        <td>snmp_interface<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>A list of interface IDs to enable SNMP. If enabling on a VLAN, use '2.3' syntax. If omitted, snmp is enabled on all interfaces</div>
        </td>
        </tr>

        <tr>
        <td>snmp_location<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>Optional SNMP location string to add the SNMP configuration</div>
        </td>
        </tr>

        </table>

    </td>
    </tr>
    </td>
    </tr>

    <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
    <td><ul><li>present</li><li>absent</li></ul></td>
	<td>
        <p>Create or delete a firewall cluster</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>tags<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Optional tags to add to this engine</p>
	</td>
	</tr>
    </td>
    </tr>

    </table>
    </br>

Examples
--------

.. code-block:: yaml

    
    - name: Firewall Template
      hosts: localhost
      gather_facts: no
      tasks:
      - name: Create a single firewall
        l3fw_cluster:
          smc_logging:
            level: 10
            path: ansible-smc.log
          antivirus: false
          backup_mgt: '2.34'
          bgp:
              announced_network:
              -   network:
                      name: foonet
                      route_map: newroutemap
              antispoofing_network:
                  group:
                  - group1
                  host:
                  - 2.2.2.3
                  network:
                  - foo
              autonomous_system:
                  as_number: 4261608949
                  comment: optional
                  name: myas
              bgp_profile: Default BGP Profile
              enabled: true
              router_id: 1.2.3.4
          cluster_mode: balancing
          comment: my new firewall
          default_nat: false
          domain_server_address:
          - 8.8.8.8
          file_reputation: false
          interfaces:
          -   interface_id: '1000'
              interfaces:
              -   nodes:
                  -   address: 100.100.100.1
                      network_value: 100.100.100.0/24
                      nodeid: 1
                  -   address: 100.100.100.2
                      network_value: 100.100.100.0/24
                      nodeid: 2
              type: tunnel_interface
              zone_ref: AWSTunnel
          -   cvi_mode: packetdispatch
              interface_id: '21'
              interfaces:
              -   cluster_virtual: 22.22.22.254
                  network_value: 22.22.22.0/24
                  nodes:
                  -   address: 22.22.22.1
                      network_value: 22.22.22.0/24
                      nodeid: 1
                  -   address: 22.22.22.2
                      network_value: 22.22.22.0/24
                      nodeid: 2
                  vlan_id: '21'
              -   cluster_virtual: 21.21.21.254
                  network_value: 21.21.21.0/24
                  nodes:
                  -   address: 21.21.21.2
                      network_value: 21.21.21.0/24
                      nodeid: 2
                  -   address: 21.21.21.1
                      network_value: 21.21.21.0/24
                      nodeid: 1
                  vlan_id: '20'
              macaddress: 02:02:02:20:20:22
          -   interface_id: '4'
              interfaces:
              -   nodes:
                  -   address: 5.5.5.2
                      network_value: 5.5.5.0/24
                      nodeid: 1
                  -   address: 5.5.5.3
                      network_value: 5.5.5.0/24
                      nodeid: 2
              zone_ref: heartbeat
          -   cvi_mode: packetdispatch
              interface_id: '0'
              interfaces:
              -   cluster_virtual: 1.1.1.1
                  network_value: 1.1.1.0/24
                  nodes:
                  -   address: 1.1.1.2
                      network_value: 1.1.1.0/24
                      nodeid: 1
                  -   address: 1.1.1.3
                      network_value: 1.1.1.0/24
                      nodeid: 2
              macaddress: 02:02:02:02:02:02
          -   comment: foocomment
              interface_id: '2'
              interfaces:
              -   comment: vlan comment
                  nodes:
                  -   address: 34.34.34.35
                      network_value: 34.34.34.0/24
                      nodeid: 2
                  -   address: 34.34.34.34
                      network_value: 34.34.34.0/24
                      nodeid: 1
                  vlan_id: '34'
              -   nodes:
                  -   address: 35.35.35.35
                      network_value: 35.35.35.0/24
                      nodeid: 1
                  -   address: 35.35.35.36
                      network_value: 35.35.35.0/24
                      nodeid: 2
                  vlan_id: '35'
          location: foolocation
          name: newcluster2
          primary_heartbeat: '4'
          primary_mgt: '0'
          snmp:
              snmp_agent: myagent
              snmp_interface:
              - '2.35'
              - '2.34'
              - '0'
              snmp_location: snmplocation
          tags:
          - footag
          #skip_interfaces: false
          #delete_undefined_interfaces: false
          #state: absent

    # Delete a cluster
    - name: firewall cluster with 3 members
      l3fw_cluster:
        name: mycluster
        state: absent


Return Values
-------------

Common return values are documented `Return Values <http://docs.ansible.com/ansible/latest/common_return_values.html>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>

    <tr>
    <td>state</td>
    <td>
        <div>Full json definition of NGFW</div>
    </td>
    <td align=center>always</td>
    <td align=center>dict</td>
    <td align=center></td>
    </tr>

    <tr>
    <td>changed</td>
    <td>
        <div>Whether or not the change succeeded</div>
    </td>
    <td align=center>always</td>
    <td align=center>bool</td>
    <td align=center></td>
    </tr>
    </table>
    </br></br>


Author
~~~~~~

    * Forcepoint


