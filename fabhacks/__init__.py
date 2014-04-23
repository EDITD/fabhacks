# Fabhacks
# File: __init__.py
# Desc: Fabric based deploy hacks

from time import sleep

from fabric.api import run, sudo, put
from fabric.context_managers import cd


# Restart something
# with a check to ensure running
def restart_confirm( check, command, backoff=0, use_sudo=False ):
    func = sudo if use_sudo else run
    func( command, pty=False )

    sleep( backoff )
    status = func( 'ps aux | grep -v grep | grep {0}'.format( check ), quiet=True, warn_only=True )
    if not status.succeeded:
        backoff += 1
        print 'Restart command failed: {0}, retrying with {1}s backoff...'.format( command, backoff )
        restart_confirm( check, command, backoff=backoff, use_sudo=use_sudo )


# Setup app user
# creates user, home directory and uploads ssh/deploy key
def create_user( username, directory, key=None, use_sudo=False ):
    func = sudo if use_sudo else run

    if not func( 'find {0}'.format( directory ), quiet=True, warn_only=True ).succeeded:
        print 'CREATE USER'
        func( 'echo -e "\n\n\n\n\n\n" | adduser {0}'.format( username ))
        # Setup SSH deploy key/etc
        func( 'mkdir -p {0}/.ssh'.format( directory ))
        func( 'chown -R {0}:{0} {1}/.ssh/'.format( username, directory ))

    # Install deploy key for GitHub => user
    if key is not None:
        put( local_path=key, remote_path='{0}/.ssh/id_rsa'.format( directory ), use_sudo=use_sudo )


# Deploy git app
# deploys and/or updates a git based application
def deploy_git( destination, user, repository, branch='master', use_sudo=False  ):
    func = sudo if use_sudo else run

    if not func( 'find {0}/.git/index'.format( destination ), quiet=True, warn_only=True ).succeeded:
        func( 'mkdir -p {0}'.format( destination ))
        func( 'chown -R {0}:{0} {1}'.format( user, destination ))
        func( 'git clone -b {0} {1} {2}'.format( branch, repository, destination ), user=user )
    else:
        with cd( destination ):
            func( 'git checkout {0}'.format( branch ), user=user )
            func( 'git pull'.format( destination ), user=user )


# Install Pip
# installs latest + installs 1.4 over the top because post-v1.4 is ruined
def install_pip( use_sudo=False ):
    func = sudo if use_sudo else run

    # Got pip already?
    if not func( 'which pip', quiet=True, warn_only=True ).succeeded:
        func( 'wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py -O /tmp/get-pip.py' )
        func( 'python /tmp/get-pip.py' )

    # Downgrade pip to something not built by idiots
    # no sane person want's to deal with --allow-unverified shit
    func( 'pip install pip==1.4' )