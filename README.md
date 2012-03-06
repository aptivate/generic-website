# Install

After cloning this project, go into the deploy directory, edit fabfile.py
and check the repository settings:

	env.repo_type = "git" or "svn"
	env.repository = 'https://' or 'git://...' or 'git@...'
	env.svnuser = '<username>' and env.svnpass = '<password>' for Subversion repositories

And the server name settings:

	env.hosts = ['server-hostname']

For servers that are configured, remove the abort() line to make
deployment work:

	utils.abort('remove this line when server is setup')

In the same directory, edit `project_settings.py` and change the project
name to something unique:

	project_name = "acme_widgets"

In the `django/website` directory, edit the `local_settings.py.*` files
and choose appropriate database settings. For example, you might well
want to use SQLite databases for development, because they require
minimal setup, and MySQL in production. You may also want to configure
SOLR instead of Whoosh as the search engine.

All of these settings are used as overrides of settings.py, so any
settings which apply to all environments can be made there. If your
production server lives in a different timezone, you may wish to
override `TIME_ZONE` in `local_settings.py.production`.

Now run these commands to generate a secret key and database password,
symlink `local_settings.py` to an environment such as `dev`, create the
database, tables and virtualenv, and download any dependent packages:

	cd deploy
	tasks.py deploy:dev
	cd ..

You'll need to create a super user to log into the django-cms admin
interface:

	cd django/website
	./manage.py createsuperuser

And then start the webserver:

	./manage.py runserver

And start hacking!
