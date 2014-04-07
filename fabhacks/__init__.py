# Fabhacks
# File: __init__.py
# Desc: Fabric based deploy hacks

from fabric.api import run, sudo


# Restart something
# with a check to ensure running
def restart_confirm( check, command, use_sudo=False ):
    func = sudo if use_sudo else run
    func( command )

    status = func( 'ps aux | grep -v grep | grep {0}'.format( check ), warn_only=True )
    if not status.succeeded:
        print 'Restart command failed: {0}, retrying...'.format( command )
        restart( check, command )


# Setup app user
# creates user, home directory and uploads ssh/deploy key
def create_user( username, directory, key=None, use_sudo=False ):
    func = sudo if use_sudo else run

    if not exists( directory, use_sudo=use_sudo ):
        func( 'echo -e "\n\n\n\n\n\n" | adduser {0}'.format( username ))
        # Setup SSH deploy key/etc
        func( 'mkdir -p {0}/.ssh'.format( directory ))
        func( 'chown -R {0}:{0} {1}/.ssh/'.format( username, directory ))
        # Install deploy key for GitHub => user
        if key is not None:
            put( local_path=key, remote_path='{0}/.ssh/id_rsa'.format( username ), use_sudo=use_sudo )


# Deploy git app
# deploys and/or updates a git based application
def deploy_git( destination, user, repository, branch='master', use_sudo=False  ):
    func = sudo if use_sudo else run

    if not exists( '/{0}.git/index'.format( destination ), use_sudo=True ):
        func( 'mkdir -p {0}'.format( destination ))
        func( 'chown -R {0}:{0} {1}'.format( user, destination ))
        func( 'git clone {0} {1}'.format( repository, destination ), user=user )
    else:
        with cd( destination ):
            func( 'git pull', user=user )