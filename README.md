# KYPO on OVN

## Standalone implementation

1. Gather required data from sandbox JSON description and generated SSH config
1. Deploy OVN across master and network hosts
1. Reattach NICs from current bridge to br-int and describe external-id [1]
1. Translate sandbox topology into OVN configuration and apply it
1. Configure interrouting
1. Configure DHCP
1. Support centrally controlled traffic shaping between hosts

## Native KYPO integration

1. Move OVN deployment to KYPO
1. Replace host NIC reattaching with direct attaching to br-int
1. Move OVN NB configuration under KYPO and trigger setup when sandbox topology changes

## Alternatives

- In order to make SDN effective (or even functional), it might be necessary to change KYPO in the way that it would create only one network host and connect all end-stations to it. If we keep current implementation we still need to configure routing in underlay and if user configures two separate network block it could be impossible to create overlay. It would also require a logical network change since OVN has logical routers and switches, while KYPO has L3 switches only.
- Another way which would keep the current KYPO network hosts would be to centrally configure routing. There could be a daemon on master host that would configure routing on network hosts in order to accomplish interconnectivity. This solution can profit from current implementation and provide traffic shaping between switches.
- A middle way would be to configure routing via openflow rules. We could create a simple controller on master host that would generate rules based on KYPO topology. Clients on network hosts could read such rules and apply them on existing OVS bridges. With this option we would implement simple L3 switch. Each switch would be connected only to hosts from one network and it will be directly attached to "underlay" leading to another L3 switch. Excuse for reimplementation is specific scenario and need for traffic shaping between switches.

## Notes

- Run tasks on network hosts in parallel

[1] https://github.com/openvswitch/ovs/blob/master/Documentation/topics/integration.rst

[2] https://docs.openstack.org/networking-ovn/latest/install/index.html#controller-nodes

[3] http://blog.spinhirne.com/2016/09/an-introduction-to-ovn-routing.html