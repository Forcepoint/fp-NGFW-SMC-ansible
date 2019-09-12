.. _route_vpn:


route_vpn - Create a route-based VPN
++++++++++++++++++++++++++++++++++++


.. contents::
   :local:
   :depth: 2


Synopsis
--------


* Create a route-based VPN. Route-based VPNs are typically created between a managed Forcepoint NGFW Engine and a third-party device, such as AWS or Azure. You must create the firewall before running this module. If you are configuring a route-based VPN tunnel of the VPN tunnel type, you must also specify an existing tunnel interface to bind and specify an IP address or interface ID to specify the ISAKMP listener.


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
    <td>enabled<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td><ul><li>yes</li><li>no</li></ul></td>
	<td>
        <p>Whether the VPN is enabled or disabled</p>
	</td>
	</tr>
    </td>
    </tr>
    <tr>
    <td rowspan="2">local_gw<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>Represents the locally managed Forcepoint NGFW Engine. If the remote_gw is also a managed device, use the same parameters to define it.</div>
    </tr>

    <tr>
    <td colspan="5">
        <table border=1 cellpadding=4>
        <caption><b>Dictionary object local_gw</b></caption>

        <tr>
        <th class="head">parameter</th>
        <th class="head">required</th>
        <th class="head">default</th>
        <th class="head">choices</th>
        <th class="head">comments</th>
        </tr>

        <tr>
        <td>tunnel_interface<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>The ID for the tunnel interface</div>
        </td>
        </tr>

        <tr>
        <td>interface_id<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>The interface ID to enable IPSec. If multiple IP addresses exist on the interface, IPSec will be enabled on all. Use <em>interface_ip</em> as an alternative.</div>
        </td>
        </tr>

        <tr>
        <td>name<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>The name of the Forcepoint NGFW Engine</div>
        </td>
        </tr>

        <tr>
        <td>address<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>An interface IP addresses to enable IPSec. Use this parameter if there are multiple IP addresses on a single interface specified with <em>interface_id</em> and you want to bind to only that address.</div>
        </td>
        </tr>

        </table>

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
        <p>The name for this route-based VPN.</p>
	</td>
	</tr>
    </td>
    </tr>
    <tr>
    <td rowspan="2">remote_gw<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
    <td></td>
    <td>
        <div>The name of the remote gateway. If the remote gateway is a Forcepoint NGFW Engine, it must  already exist. See the local_gw documentation for settings. If the remote gateway is an external VPN gateway, this module will create the gateway based on the gateway settings provided if it does not already exist. This documents an external VPN gateway configuration. See also the external_gateway module for additional external endpoint settings.</div>
    </tr>

    <tr>
    <td colspan="5">
        <table border=1 cellpadding=4>
        <caption><b>Dictionary object remote_gw</b></caption>

        <tr>
        <th class="head">parameter</th>
        <th class="head">required</th>
        <th class="head">default</th>
        <th class="head">choices</th>
        <th class="head">comments</th>
        </tr>

        <tr>
        <td>preshared_key<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>If this is an external VPN gateway, you must provide a pre-shared key to be used between the gateways. If the gateway is another Forcepoint NGFW Engine, a key will be auto-generated.</div>
        </td>
        </tr>

        <tr>
        <td>external_endpoint<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>The external endpoint where the route-based VPN will terminate. Any options that are supported by the smcpython ExternalEndpoint.create constructor are supported values for this definition.</div>
        </td>
        </tr>

        <tr>
        <td>type<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>Set to external_gateway if this is an external VPN gateway element</div>
        </td>
        </tr>

        <tr>
        <td>vpn_site<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
        <td></td>
        <td>
            <div>Defines the VPN site for the protected networks on other end of external VPN gateway</div>
        </td>
        </tr>

        <tr>
        <td>name<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
        <td></td>
        <td>
            <div>The name of the external VPN gateway. If the external VPN gateway element does not exist, it will be created if you provide the address and networks parameters.</div>
        </td>
        </tr>

        </table>

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
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
    <td><ul><li>present</li><li>absent</li></ul></td>
	<td>
        <p>Specify a create or delete operation</p>
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
        <p>Provide an optional category tag to the engine. If the category does not exist, it will be created</p>
	</td>
	</tr>
    </td>
    </tr>

    <tr>
    <td>type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>ipsec</td>
    <td><ul><li>ipsec</li><li>gre</li></ul></td>
	<td>
        <p>The type of route-based VPN tunnel to create</p>
	</td>
	</tr>
    </td>
    </tr>

    </table>
    </br>

Examples
--------

.. code-block:: yaml

    
    - name: Route VPN between internal engine and 3rd party external gateway
      register: result
      route_vpn:
        smc_logging:
          level: 10
          path: ansible-smc.log
        enabled: true
        local_gw:
            address: 50.50.50.1
            name: newcluster
            tunnel_interface: '1001'
        name: myrbvpn
        remote_gw:
            external_endpoint:
            -   address: 33.33.33.41
                enabled: true
                name: extgw3 (33.33.33.41)
                connection_type: 'Active 1'
            -   address: 34.34.34.34
                enabled: true
                name: endpoint2 (34.34.34.34)
                connection_type: 'Active 1'
            -   address: 44.44.44.44
                enabled: false
                name: extgw4 (44.44.44.44)
                connection_type: 'Active 1'
            -   address: 33.33.33.50
                enabled: false
                name: endpoint1 (33.33.33.50)
                connection_type: 'Active 1'
            name: extgw3
            preshared_key: '********'
            type: external_gateway
            vpn_site:
                name: extgw3-site
                network:
                - network-172.18.15.0/24
                - network-172.18.1.0/24
                - network-172.18.2.0/24

    - name: Create a new Route VPN with internal gateways
      route_vpn:
        smc_logging:
          level: 10
          path: ansible-smc.log
        name: myrbvpn
        type: ipsec
        local_gw:
          name: newcluster
          tunnel_interface: 1001
          interface_id: 1
          #address: 2.2.2.2
        remote_gw:
          name: myfw
          tunnel_interface: 1000
          interface_id: 0  
      tags:
        - footag     


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
        <div>The current state of the element</div>
    </td>
    <td align=center></td>
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


Notes
-----

.. note::
    - Login credential information is either obtained by providing them directly to the task/play, specifying an alt_filepath to read the credentials from to the play, or from environment variables (in that order). See http://smc-python.readthedocs.io/en/latest/pages/session.html for more information.


Author
~~~~~~

    * Forcepoint




Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


