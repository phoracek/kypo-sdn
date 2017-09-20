import json

from fabric.api import env, task, run, execute, roles

from . import _aptget, _systemctl, _firewalld, _ovs

KYPO_CONFIG_PATH = './kypo_config.json'
SSH_CONFIG_PATH = './ssh_config'


# TODO: this is not the ideal way, trying to be standalone
# replaces proper access to resources, info about nodes,...
def _init_data():
    with open(KYPO_CONFIG_PATH) as kypo_config_file:
        _kypo_config = json.load(kypo_config_file)

    kypo_networks = {
        network['name'] for network in _kypo_config['networks']['networks']}
    kypo_hosts = {
        network['name'] for network in _kypo_config['hosts']['hosts']}

    _master_host = None
    _network_hosts = []

    with open(SSH_CONFIG_PATH) as ssh_config_file:
        for line in ssh_config_file.readlines():
            if not line.startswith('Host'):
                continue
            host_name = line.split()[1]
            if _host_matches(host_name, kypo_networks):
                _network_hosts.append(host_name)
            elif not _host_matches(host_name, kypo_hosts):
                _master_host = host_name

    return _kypo_config, _master_host, _network_hosts


def _host_matches(host_name, type_members):
    for member in type_members:
        if host_name.endswith(member):
            return True
    return False

# TODO: try to get rid of globals, better have it memoized
kypo_config, master_host, network_hosts = _init_data()

env.roledefs = {
    'master': [master_host],
    'network': network_hosts,
    'host': []
}


@task
def setup():
    env.user = 'root'

    execute(_deploy_master)
    execute(_deploy_nodes)
    execute(_attach_endpoints)
    execute(_set_topology)
    execute(_set_routing)
    execute(_set_dhcp)
    execute(_set_shaping)


@roles('master')
def _deploy_master():
    _aptget.ensure_installed('openvswitch-ovn', 'networking-ovn')
    _systemctl.ensure_started_and_enabled('openvswitch')
    _firewalld.ensure_opened_tcp(6640)  # TODO: 41 and 42 ?
    # TODO: get address from networks network
    _ovs.ensure_remotely_accessible('IP_ADDRESS_TODO', 6640)
    run('ovs-appctl -t ovsdb-server ovsdb-server/add-remote ptcp:6640:IP_ADDRESS_TODO')  # TODO: if needed
    _systemctl.ensure_started_and_enabled('ovn-northd')


@roles('network')
def _deploy_nodes():
    _aptget.ensure_installed('openvswitch-ovn', 'networking-ovn')
    _systemctl.ensure_started_and_enabled('openvswitch')
    # TODO: get ip of master
    _ovs.ensure_external_id('ovn-remote', 'tcp:IP_ADDRESS:6642')
    _ovs.ensure_external_id('ovn-encap-type', 'geneve')
    # TODO: get IP of data network
    _ovs.ensure_external_id('ovn-encap-ip', 'IP_ADDRESS')
    _systemctl.ensure_started_and_enabled('ovn-controller')

    # TODO: https://github.com/openvswitch/ovs/blob/master/Documentation/topics/integration.rst
    # TODO: set bridge id?


@roles('network')
def _attach_endpoints():
    # TODO: move endpoints from previous ovs bridge to ovn
    # TODO: make sure to set correct external ids
    pass
    # TODO: https://github.com/openvswitch/ovs/blob/master/Documentation/topics/integration.rst
    # TODO: attached-mac
    # TODO: iface-id
    # TODO: iface-status
    # TODO: vm-id


@roles('master')
def _set_topology():
    running_lss, running_lrs = _get_running_ovn_topology()
    desired_lss, desired_lrs = _decode_desired_ovn_topology()

    lss_to_remove = set(running_lss) - set(desired_lss)
    lrs_to_remove = set(running_lrs) - set(desired_lrs)
    lss_to_add = set(desired_lss) - set(running_lss)
    lrs_to_add = set(desired_lrs) - set(running_lrs)

    # TODO: remove and add/remove whole ls/lr

    # TODO: iterate desired and adjust ports


# http://blog.spinhirne.com/2016/09/an-introduction-to-ovn-routing.html
# TODO: one router and switch per network (l3 switches)
def _get_running_ovn_topology():
    lss = {
        'switch1': [
            ('name', 'address')
        ]
    }
    lrs = {}
    return lss, lrs


def _decode_desired_ovn_topology():
    # TODO: one switch per network, one router per route
    lss = {}
    lrs = {}
    return lss, lrs


@roles('master')
def _set_dhcp():
    pass


@roles('master')
def _set_routing():
    # TODO: calculate routes for interconnectivity
    pass


@roles('network')
def _set_shaping():
    # TODO: set shaping on endpoint ifaces
    pass
