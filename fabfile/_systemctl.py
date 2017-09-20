from fabric.api import run


def is_running(service_name):
    return True


def is_enabled(service_name):
    return True


def start(service_name):
    run('systemctl start {}'.format(service_name))


def enable(service_name):
    run('systemctl enable {}'.format(service_name))


def ensure_started_and_enabled(*service_names):
    for service_name in service_names:
        if not is_running(service_name):
            start(service_name)
        if not is_enabled(service_name):
            enable(service_name)
