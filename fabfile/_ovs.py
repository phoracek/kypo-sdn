def ensure_remotely_accessible(address, port):
    pass
    run('ovs-appctl -t ovsdb-server ovsdb-server/add-remote ptcp:6640:IP_ADDRESS_TODO')  # TODO: if needed


def ensure_external_id(key, value):
    pass
    run('ovs-vsctl set open . external-ids:ovn-encap-ip=IP_ADDRESS')  # TODO: if needed