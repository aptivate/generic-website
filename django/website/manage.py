#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from os import path

# check python version is high enough
MIN_PYTHON_MINOR_VERSION = 6
if sys.version_info[0] != 2:
    print >> sys.stderr, "Arrggh - not using python 2.x"
    sys.exit(1)
if sys.version_info[1] < MIN_PYTHON_MINOR_VERSION:
    print >> sys.stderr, "You must use python 2.%d or later, you are using 2.%d" % (
            MIN_PYTHON_MINOR_VERSION, sys.version_info[1])
    sys.exit(1)

PROJECT_ROOT = path.abspath(path.dirname(__file__))
DEPLOY_DIR = path.abspath(path.join(PROJECT_ROOT, '..', '..', 'deploy'))

# ignore the usual virtualenv
# note that for runserver Django will start a child process, so that it
# can kill and restart the child process. So we use the environment to pass
# the argument along.
if '--ignore-ve' in sys.argv:
    sys.argv.remove('--ignore-ve')
    os.environ['IGNORE_DOTVE'] = 'true'

if 'IGNORE_DOTVE' not in os.environ:
    import shutil, subprocess
    REQUIREMENTS = path.join(DEPLOY_DIR, 'pip_packages.txt')
    VE_ROOT = path.join(PROJECT_ROOT, '.ve')
    VE_TIMESTAMP = path.join(VE_ROOT, 'timestamp')

    def update_ve_timestamp():
        file(VE_TIMESTAMP, 'w').close()

    def virtualenv_needs_update():
        # timestamp of last modification of .ve/ directory
        ve_dir_mtime = path.exists(VE_ROOT) and path.getmtime(VE_ROOT) or 0
        # timestamp of last modification of .ve/timestamp file (touched by this
        # script
        ve_timestamp_mtime = path.exists(VE_TIMESTAMP) and path.getmtime(VE_TIMESTAMP) or 0
        # timestamp of requirements file (pip_packages.txt)
        reqs_timestamp = path.getmtime(REQUIREMENTS)
        # if the requirements file is newer than the virtualenv directory,
        # then the virtualenv needs updating
        if ve_dir_mtime < reqs_timestamp:
            return True
        # if the requirements file is newer than the virtualenv timestamp file,
        # then the virtualenv needs updating
        elif ve_timestamp_mtime < reqs_timestamp:
            return True
        else:
            return False

    def go_to_ve():
        """
        If running inside virtualenv already, then just return and carry on.

        If not inside the virtualenv then call the virtualenv python, pass it
        this file and all the arguments to it, so this file will be run inside
        the virtualenv.
        """
        if 'IN_VIRTUALENV' not in os.environ:
            if sys.platform == 'win32':
                python = path.join(VE_ROOT, 'Scripts', 'python.exe')
            else:
                python = path.join(VE_ROOT, 'bin', 'python')

            # add environment variable to say we are now in virtualenv
            new_env = os.environ
            new_env['IN_VIRTUALENV'] = 'true'
            retcode = subprocess.call([python, __file__] + sys.argv[1:],
                    env=new_env)
            sys.exit(retcode)

    # manually update virtualenv?
    update_ve = 'update_ve' in sys.argv or 'update_ve_quick' in sys.argv
    # destroy the old virtualenv so we have a clean virtualenv?
    destroy_old_ve = 'update_ve' in sys.argv
    # check if virtualenv needs updating and only proceed if it is required
    update_required = virtualenv_needs_update()
    # or just do the update anyway
    force_update = '--force' in sys.argv

    # we've been told to update the virtualenv AND
    # EITHER it needs an update OR the update is forced
    if update_ve:
        if not update_required and not force_update:
            print "VirtualEnv does not need to be updated"
            print "use --force to force an update"
            sys.exit(0)
        # if we need to create the virtualenv, then we must do that from
        # outside the virtualenv. The code inside this if statement will only
        # be run outside the virtualenv.
        if destroy_old_ve and path.exists(VE_ROOT):
            shutil.rmtree(VE_ROOT)
        if not path.exists(VE_ROOT):
            import virtualenv
            virtualenv.logger = virtualenv.Logger(consumers=[])
            #virtualenv.create_environment(VE_ROOT, site_packages=True)
            virtualenv.create_environment(VE_ROOT, site_packages=False)

        # install the pip requirements and exit
        pip_path = path.join(VE_ROOT, 'bin', 'pip')
        # use cwd to allow relative path specs in requirements file, e.g. ../tika
        pip_retcode = subprocess.call([pip_path, 'install',
                '--requirement=%s' % REQUIREMENTS ],
                cwd=os.path.dirname(REQUIREMENTS))
        if pip_retcode == 0:
            update_ve_timestamp()
        sys.exit(pip_retcode)
    # else if it appears that the virtualenv is out of date:
    elif update_required:
        print "VirtualEnv need to be updated"
        print 'Run "./manage.py update_ve" (or "./manage.py update_ve_quick")'
        sys.exit(1)

    # now we should enter the virtualenv. We will only get
    # this far if the virtualenv is up to date.
    go_to_ve()

# run django
from django.core.management import setup_environ, ManagementUtility

try:
    import settings # Assumed to be in the same directory.
except ImportError as e:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n%s\n" % (__file__, e))
    sys.exit(1)

def execute_manager(settings_mod, argv=None):
    """
    Like execute_from_command_line(), but for use by manage.py, a
    project-specific django-admin.py utility.
    """
    
    # don't add the project directory to the environment, as this ends
    # up importing classes using the project name, and self.assertIsInstance
    # requires us to specify the project name, making our tests non-portable.
    # setup_environ(settings_mod)
    
    # No monkey patches yet :)
    # import binder.monkeypatch
    # But we do need to do this first:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    utility = ManagementUtility(argv)
    utility.execute()

if __name__ == "__main__":
    execute_manager(settings)
