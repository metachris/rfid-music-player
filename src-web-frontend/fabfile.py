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
DIR_REMOTE = "/server/rfid-music-player/web-frontend"

env.use_ssh_config = True
if not env.hosts:
    # Set default host to something
    env.hosts = ["roberry"]

@task
def build():
    """ Upload sources to a Raspberry """
    local("yarn run build")

@task
def upload(build_first=False):
    """ Upload sources to a Raspberry """
    if build_first:
        build()
    put("dist/*", DIR_REMOTE, mirror_local_mode=True, use_sudo=True)
