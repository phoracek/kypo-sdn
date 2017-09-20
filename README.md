# KYPO on OVN

## Standalone implementation

1. Gather required data from sandbox JSON description and generated SSH config
1. Deploy OVN across master and network hosts
1. Reattach NICs from current bridge to br-int and describe external-id [1]
1. Translate sandbox topology into OVN configuration and apply it
1. Configure L3 interconnectivity
1. Configure DHCP
1. Support centrally controlled traffic shaping between hosts

## Native KYPO integration

1. Move OVN deployment to KYPO
1. Replace host NIC reattaching with direct attaching to br-int
1. Move OVN NB configuration under KYPO and trigger setup when sandbox topology changes, pass required data directly

## Notes

- Run tasks on network hosts in parallel

[1] https://github.com/openvswitch/ovs/blob/master/Documentation/topics/integration.rst

[2] https://docs.openstack.org/networking-ovn/latest/install/index.html#controller-nodes

[3] http://blog.spinhirne.com/2016/09/an-introduction-to-ovn-routing.html

## Why not SDN

SDN requires one interconnected data network. In current KYPO it would require us to use management network for data or to configure underlay routing before we deploy overlay (but even that might not work out in case of two separate network blocks).

Another issue with SDN would be problematic traffic shaping between network nodes. There is one underlay network for all virtual networks, there is no designated interface per network that would allow us to set network parameters.

## Why not OpenFlow routing

Another option would be to introduce our own controller that would configure routing on OVS switches via OpenFlow. That would require us not only to implement routing rules, but also ARP handling. (Maybe it would be necessary to implement L2-learning switch as well.)

## Viable solution (?)

Best solution seems to be to use plain linux routing that would have routes calculated centrally. We would have one script on master node that would translate sandbox topology JSON into specific configuration per network host (routes to accomplish interconnectivity, which ifaces should be connected to switch, traffic shaping, bondings, dhcp,...). Another script would be deployed on all network hosts and it would accept specific configuration from master script and apply it.

With this solution we would use maximum of currently implemented KYPO features. It would also be easy to switch from OVS switch to linux bridge. It can be implemented in form of remotely executed scripts or as a client-server based services.