from fabric.api import *
from fabric import utils
from fabric.decorators import hosts

# this is our common file that can be copied across projects
# we deliberately import all of this to get all the commands it
# provides as fabric commands
from fablib import *
import fablib

# project_settings - try not to repeat ourselves so much ...
import project_settings

env.home = '/var/django/'
env.project = project_settings.project_name
# the top level directory on the server
env.project_dir = env.project

# repository type can be "svn" or "git"
env.repo_type = "git"
env.repository = 'FIXME git://github.com/aptivate/generic-website.git'

env.django_dir = project_settings.django_dir
env.test_cmd = ' manage.py test -v0 ' + ' '.join(project_settings.django_apps)

env.project_type = project_settings.project_type

# does this virtualenv for python packages
env.use_virtualenv = True

# valid environments - used for require statements in fablib
env.valid_non_prod_envs = ('dev_server', 'staging_test', 'staging')
env.valid_envs = ('dev_server', 'staging_test', 'staging', 'production')

# does this use apache - mostly for staging_test
env.use_apache = True


# this function can just call the fablib _setup_path function
# or you can use it to override the defaults
def _local_setup():
    # put your own defaults here
    fablib._setup_path()
    # override settings here
    # if you have an ssh key and particular user you need to use
    # then uncomment the next 2 lines
    #env.user = "root" 
    #env.key_filename = ["/home/shared/keypair.rsa"]


#
# These commands set up the environment variables
# to be used by later commands
#

def dev_server():
    """ use dev environment on remote host to play with code in production-like env"""
    utils.abort('remove this line when server is setup')
    env.environment = 'dev_server'
    env.hosts = ['fen-vz-%s-dev.fen.aptivate.org' % project_settings.project_name]
    _local_setup()


def staging_test():
    """ use staging environment on remote host to run tests"""
    # this is on the same server as the customer facing stage site
    # so we need project_root to be different ...
    utils.abort('remove this line when server is setup')
    env.project_dir = env.project + '_test'
    env.environment = 'staging_test'
    env.use_apache = False
    env.hosts = ['fen-vz-%s.fen.aptivate.org' % project_settings.project_name]
    _local_setup()


def staging():
    """ use staging environment on remote host to demo to client"""
    utils.abort('remove this line when server is setup')
    env.environment = 'staging'
    env.hosts = ['fen-vz-%s.fen.aptivate.org' % project_settings.project_name]
    _local_setup()


def production():
    """ use production environment on remote host"""
    utils.abort('remove this line when server is setup')
    env.environment = 'production'
    env.hosts = ['lin-%s.aptivate.org:48001' % project_settings.project_name]
    _local_setup()


def deploy(revision=None, keep=None):
    """ update remote host environment (virtualenv, deploy, update)

    It takes two arguments:

    * revision is the VCS revision ID to checkout (if not specified then
      the latest will be checked out)
    * keep is the number of old versions to keep around for rollback (default
      5)"""
    require('project_root', provided_by=env.valid_envs)
    fablib.check_for_local_changes()
    fablib._create_dir_if_not_exists(env.project_root)

    if files.exists(env.vcs_root):
        create_copy_for_rollback(keep)

    # don't need to stop apache until rollback copy created
    with settings(warn_only=True):
        apache_cmd('stop')

    checkout_or_update(revision)
    if env.use_virtualenv:
        update_requirements()

    # if we're going to call tasks.py then this has to be done first:
    create_private_settings()
    link_local_settings()

    update_db(force_use_migrations=True)

    rm_pyc_files()
    if env.environment == 'production':
        setup_db_dumps()

    link_apache_conf()
    apache_cmd('start')


