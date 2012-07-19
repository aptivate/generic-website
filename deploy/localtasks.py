import tasklib


def deploy(environment=None):
    """Do all the required steps in order"""
    if environment == None:
        environment = tasklib._infer_environment()

    tasklib.create_private_settings()
    tasklib.link_local_settings(environment)
    tasklib.update_git_submodules()
    tasklib.create_ve()
    tasklib.update_db(force_use_migrations=True)
