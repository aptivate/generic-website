import os, sys, site

# find the project name from project_settings
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(os.path.join(project_dir, 'deploy'))
from project_settings import project_name, django_dir

# ensure the virtualenv for this instance is added
site.addsitedir(os.path.join(project_dir, django_dir, '.ve', 'lib',
    'python2.6', 'site-packages'))

# not sure about this - might be required for packages installed from
# git/svn etc
#site.addsitedir(os.path.join(project_dir, 'django', project_name, '.ve', 'src'))
sys.path.append(os.path.join(project_dir, django_dir))

# this basically does:
# os.environ['PROJECT_NAME_HOME'] = '/var/django/project_name/dev/'
os.environ[project_name.upper() + '_HOME'] = project_dir

# this does the same setup as "./manage.py runserver", ensuring we get the
# same behaviour on apache as when developing.
# See http://blog.dscpl.com.au/2010/03/improved-wsgi-script-for-use-with.html
# for the rationale.

import settings

import django.core.management

# don't add the project directory to the environment, as this ends
# up importing classes using the project name, and self.assertIsInstance
# requires us to specify the project name, making our tests non-portable.
#
# sys.path.append(os.path.join(project_dir, 'django'))
# django.core.management.setup_environ(settings)

# We don't include the project parent directory in PYTHONPATH, so we
# can't import the settings module as project_name.settings.
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

utility = django.core.management.ManagementUtility()
command = utility.fetch_command('runserver')
command.validate()

import django.conf
import django.utils
django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)

# Now we do the normal django set up
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

# Dozer is something that can help debug memory leaks
#from dozer import Dozer
#application = Dozer(application)
