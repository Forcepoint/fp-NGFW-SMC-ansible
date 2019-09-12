.. _engine_facts:


engine_facts - Facts about NGFW Engines configured in the SMC
++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::
   :local:
   :depth: 2


Synopsis
--------


* An NGFW Engine is any device that is configured and managed using the SMC. An NGFW Engine can be physical or virtual, a single engine or a cluster, and can be a firewall, IPS, or layer 2 firewall.


Requirements (on host that executes module)
-------------------------------------------

  * smc-python version 0.6.0 or greater


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
    <td>case_sensitive<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
    <td></td>
	<td>
        <p>Whether to do a case sensitive match on the filter specified</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>element<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>engine_clusters</td>
    <td><ul><li>engine_clusters</li><li>layer2_clusters</li><li>ips_clusters</li><li>fw_clusters</li></ul></td>
	<td>
        <p>Type of engine to search for</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>exact_match<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
	<td>
        <p>Whether to do an exact match on the filter specified</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>filter<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>*</td>
    <td></td>
	<td>
        <p>String value to match against when making query. Matches all if not specified. A filter will attempt to find a match in the name, primary key field or comment field of a given record.</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>10</td>
    <td></td>
	<td>
        <p>Limit the number of results. Set to 0 to remove limit.</p>
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
        <p>Provide an alternate path location to read the credentials from. File is expected to be stored in ~.smcrc. If provided, address and api_key settings are not required and will be ignored.</p>
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
        <p>API key for api client. The default value is the environment variable <code>SMC_API_KEY</code> Required if the <em>address</em> parameter is defined</p>
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
        <p>Optional SMC API version to connect to. If none is provided, the latest long-term support (LTS) version of the SMC API will be used based on the SMC version. Can be set though the environment variable <code>SMC_API_VERSION</code></p>
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
        <p>Optional administrative domain in the SMC to log on to. If no domain is provided, 'Shared Domain' is used. Can be set through the environment variable <code>SMC_DOMAIN</code></p>
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
        <div>Extra arguments to pass to the login constructor. These arguments are generally only used if specifically requested by support personnel.</div>
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
            <div>If the connection to the SMC API is HTTPS, you can set this to True, or provide a path to a client certificate to verify the SMC SSL certificate. You can also explicitly set this to False.</div>
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
        <p>Optional timeout for connections to the SMC API. Can be set through the environment variable <code>SMC_TIMEOUT</code></p>
	</td>
	</tr>
    </td>
    </tr>

    </table>
    </br>

Examples
--------

.. code-block:: yaml

    
    - name: Facts about all engines within SMC
      hosts: localhost
      gather_facts: no
      tasks:
      - name: Find all managed engines (IPS, Layer 2, L3FW)
        engine_facts:
      
      - name: Find a firewall cluster named mycluster
        engine_facts:
          element: fw_clusters
          filter: mycluster
      
      - name: Find only Layer 2 firewalls
        engine_facts:
          element: layer2_clusters

      - name: Find only IPS engines
        engine_facts:
          element: ips_clusters
      
      - name: Get engine details for 'myfirewall'
        engine_facts:
          filter: myfirewall

      - name: Get engine details for 'myfw' and save in editable YAML format
        register: results
        engine_facts:
          smc_logging:
            level: 10
            path: ansible-smc.log
          filter: newcluster
          as_yaml: true

      - name: Write the yaml using a jinja template
        template: src=templates/engine_yaml.j2 dest=./l3fw_cluster.yml


Return Values
-------------

Return values that are common to all modules are documented in `Return Values <http://docs.ansible.com/ansible/latest/common_return_values.html>`_. The following fields are unique to this module:

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
    <td>engines</td>
    <td>
        <div>When using a filter match, full engine json is returned</div>
    </td>
    <td align=center>always</td>
    <td align=center>list</td>
    <td align=center>[{'default_nat': True, 'name': 'myfw3', 'interfaces': [{'interfaces': [{'nodes': [{'address': '1.1.1.1', 'nodeid': 1, 'network_value': '1.1.1.0/24'}]}], 'interface_id': '0'}, {'interfaces': [{'nodes': [{'address': '10.10.10.1', 'nodeid': 1, 'network_value': '10.10.10.1/32'}]}], 'type': 'tunnel_interface', 'interface_id': '1000'}, {'interfaces': [{'nodes': [{'address': '2.2.2.1', 'nodeid': 1, 'network_value': '2.2.2.0/24'}]}], 'interface_id': '1'}], 'snmp': {'snmp_agent': 'fooagent', 'snmp_interface': ['1'], 'snmp_location': 'test'}, 'antivirus': True, 'bgp': {'router_id': '1.1.1.1', 'bgp_peering': [{'name': 'bgppeering', 'interface_id': '1000'}], 'announced_network': [{'network': {'route_map': 'myroutemap', 'name': 'network-1.1.1.0/24'}}], 'enabled': True, 'autonomous_system': {'comment': None, 'as_number': 200, 'name': 'as-200'}, 'bgp_profile': 'Default BGP Profile'}, 'file_reputation': True, 'policy_vpn': [{'mobile_gateway': False, 'satellite_node': False, 'name': 'ttesst', 'central_node': True}], 'primary_mgt': '0', 'antispoofing_network': {'network': ['network-1.1.1.0/24']}, 'type': 'single_fw', 'domain_server_address': ['8.8.8.8']}]</td>
    </tr>
    </table>
    </br></br>


Notes
-----

.. note::
    - If a filter is not used in the query, this will return all results for the element type specified. The return data in this case will only contain the metadata for the element which will be name and type. To get detailed information about an element, use a filter. When using filters on network or service elements, the filter value will search the element fields, for example, you could use a filter of '1.1.1.1' when searching for hosts and all hosts with this IP will be returned. The same applies for services. If you are unsure of the service name but know the port you require, your filter can be by port.


Author
~~~~~~

    * Forcepoint




Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


