from fabric.api import run


def is_installed(package_name):
    # TODO: apt-cache
    output = run('apt-cache')
    return False


def install(package_name):
    run('apt-get install -y {}'.format(package_name))


def ensure_installed(*package_names):
    for package_name in package_names:
        if not is_installed(package_name):
            install(package_name)
