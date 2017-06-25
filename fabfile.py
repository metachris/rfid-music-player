import os
from fabric.api import local, run, env, task
from fabric.context_managers import cd, lcd
from fabric.operations import put, get
from fabric.decorators import parallel
from fabric.contrib.project import upload_project

# Change to fabfile directory, to make relative paths work
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(DIR_SCRIPT))

# LOGFILE = "/var/log/mirapi/mirapi.log"
DIR_REMOTE = "/server/rfid-music-player"

env.use_ssh_config = True
if not env.hosts:
    # Set default host to something
    env.hosts = ["roberry"]

@task
@parallel
def deploy():
    """ Upload sources to a Raspberry """
    run("rw")
    with cd(DIR_REMOTE):
        run("git pull")
        run("player restart")
