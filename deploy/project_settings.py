# this is for settings to be used by tasks.py

# This is the name of the directory to be deployed under /var/django on
# the staging and production servers. It should be unique to allow
# different projects to be installed on the same webserver, and give
# some warning if you're about to mess up the wrong project on the
# wrong server.
project_name = "generic-website"

# put "django" here if you want django specific stuff to run
# put "plain" here for a basic apache app
project_type = "django"

# This is the directory inside the project dev dir that contains the django
# application. I declare it "website" by convention.
django_dir   = "django/website"

django_apps  = []
